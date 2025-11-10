from fastapi import FastAPI, APIRouter, HTTPException, UploadFile, File
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
import uuid
from datetime import datetime, timezone
import httpx
import asyncio
import json

# Import API tool definitions
from api_tools import SCENARIO_TOOLS, PANEL_TOOLS, RULE_TOOLS, ALL_TOOLS

# Import system prompts
from system_prompts import PRICING_ANALYST_PROMPT, DEMO_RESPONSE_TEMPLATE

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Scenario API configuration
SCENARIO_API_BASE_URL = os.environ.get('SCENARIO_API_BASE_URL', 'http://localhost:5050')
SCENARIO_API_TENANT = os.environ.get('SCENARIO_API_TENANT', 'meijer')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Models
class Chat(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ChatCreate(BaseModel):
    title: str = "New chat"

class Message(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    chat_id: str
    role: str  # "user" or "assistant"
    content: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class MessageCreate(BaseModel):
    content: str

class StreamResponse(BaseModel):
    content: str
    done: bool

# Tool Execution Functions
async def execute_tool_call(tool_name: str, tool_args: dict) -> dict:
    """
    Execute the actual API call to the Scenario API based on tool name and arguments.
    """
    headers = {
        "X-Bungee-Tenant": SCENARIO_API_TENANT,
        "Content-Type": "application/json"
    }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            if tool_name == "list_scenarios":
                # Build query parameters
                params = {}
                if "active" in tool_args:
                    params["active"] = str(tool_args["active"]).lower()
                if "approved" in tool_args:
                    params["approved"] = str(tool_args["approved"]).lower()
                if "scenario_type" in tool_args:
                    params["scenario_type"] = tool_args["scenario_type"]
                if "page" in tool_args:
                    params["page"] = tool_args["page"]
                if "size" in tool_args:
                    params["size"] = tool_args["size"]

                url = f"{SCENARIO_API_BASE_URL}/api/v1/pricing-rules/scenario"
                response = await client.get(url, headers=headers, params=params)
                response.raise_for_status()
                return {"success": True, "data": response.json()}

            elif tool_name == "get_scenario":
                scenario_id = tool_args.get("scenario_id")
                url = f"{SCENARIO_API_BASE_URL}/api/v1/pricing-rules/scenario/{scenario_id}"
                response = await client.get(url, headers=headers)
                response.raise_for_status()
                return {"success": True, "data": response.json()}

            elif tool_name == "create_scenario":
                url = f"{SCENARIO_API_BASE_URL}/api/v1/pricing-rules/scenario"
                response = await client.post(url, headers=headers, json=tool_args)
                response.raise_for_status()
                return {"success": True, "data": response.json()}

            # Panel API Tools
            elif tool_name == "list_panels":
                # Build query parameters for panels
                params = {}

                # Required parameter
                if "scenario" in tool_args:
                    params["scenario"] = tool_args["scenario"]

                # Optional filters
                if "panel_name" in tool_args:
                    params["panel_name"] = tool_args["panel_name"]
                if "valid" in tool_args:
                    params["valid"] = str(tool_args["valid"]).lower()

                # Product hierarchy filters
                if "department" in tool_args:
                    params["department"] = tool_args["department"]
                if "category" in tool_args:
                    params["category"] = tool_args["category"]
                if "sub_category" in tool_args:
                    params["sub_category"] = tool_args["sub_category"]
                if "sub_sub_category" in tool_args:
                    params["sub_sub_category"] = tool_args["sub_sub_category"]
                if "major_department" in tool_args:
                    params["major_department"] = tool_args["major_department"]

                # Product group filters
                if "product_group" in tool_args:
                    params["product_group"] = tool_args["product_group"]
                if "product_source" in tool_args:
                    params["product_source"] = tool_args["product_source"]

                # Location hierarchy filters
                if "zone" in tool_args:
                    params["zone"] = tool_args["zone"]
                if "zone_group" in tool_args:
                    params["zone_group"] = tool_args["zone_group"]
                if "location_hierarchy_id" in tool_args:
                    params["location_hierarchy_id"] = tool_args["location_hierarchy_id"]

                # Market group filters
                if "market_group" in tool_args:
                    params["market_group"] = tool_args["market_group"]
                if "market_source" in tool_args:
                    params["market_source"] = tool_args["market_source"]

                # Rule filters
                if "price_type" in tool_args:
                    params["price_type"] = tool_args["price_type"]
                if "rule_type" in tool_args:
                    params["rule_type"] = tool_args["rule_type"]
                if "rule_sub_type" in tool_args:
                    params["rule_sub_type"] = tool_args["rule_sub_type"]

                # Pagination and sorting
                if "page" in tool_args:
                    params["page"] = tool_args["page"]
                if "size" in tool_args:
                    params["size"] = tool_args["size"]
                if "sort" in tool_args:
                    params["sort"] = tool_args["sort"]

                url = f"{SCENARIO_API_BASE_URL}/api/v1/pricing-rules/panel"
                response = await client.get(url, headers=headers, params=params)
                response.raise_for_status()
                return {"success": True, "data": response.json()}

            elif tool_name == "get_panel":
                panel_id = tool_args.get("panel_id")
                url = f"{SCENARIO_API_BASE_URL}/api/v1/pricing-rules/panel/{panel_id}"
                response = await client.get(url, headers=headers)
                response.raise_for_status()
                return {"success": True, "data": response.json()}

            elif tool_name == "create_panel":
                url = f"{SCENARIO_API_BASE_URL}/api/v1/pricing-rules/panel"
                response = await client.post(url, headers=headers, json=tool_args)
                response.raise_for_status()
                return {"success": True, "data": response.json()}

            elif tool_name == "update_panel":
                panel_id = tool_args.get("panel_id")
                url = f"{SCENARIO_API_BASE_URL}/api/v1/pricing-rules/panel/{panel_id}"

                # Remove panel_id from the request body as it's in the URL
                update_data = {k: v for k, v in tool_args.items() if k != "panel_id"}

                response = await client.patch(url, headers=headers, json=update_data)
                response.raise_for_status()
                return {"success": True, "data": response.json()}

            elif tool_name == "delete_panel":
                panel_id = tool_args.get("panel_id")
                # IMPORTANT: Always soft delete (never use hard_delete=true)
                url = f"{SCENARIO_API_BASE_URL}/api/v1/pricing-rules/panel/{panel_id}"
                response = await client.delete(url, headers=headers)
                response.raise_for_status()
                return {"success": True, "data": response.json()}

            elif tool_name == "list_panel_rules":
                panel_id = tool_args.get("panel_id")

                # Build query parameters
                params = {}
                if "page" in tool_args:
                    params["page"] = tool_args["page"]
                if "size" in tool_args:
                    params["size"] = tool_args["size"]
                if "order_by" in tool_args:
                    params["order_by"] = tool_args["order_by"]
                if "sort_order" in tool_args:
                    params["sort_order"] = tool_args["sort_order"]

                url = f"{SCENARIO_API_BASE_URL}/api/v1/pricing-rules/panel/{panel_id}/rules"
                response = await client.get(url, headers=headers, params=params)
                response.raise_for_status()
                return {"success": True, "data": response.json()}

            # Rule API Tools
            elif tool_name == "create_cpi_rule":
                url = f"{SCENARIO_API_BASE_URL}/api/v1/pricing-rules/rule/cpi"
                response = await client.post(url, headers=headers, json=tool_args)
                response.raise_for_status()
                return {"success": True, "data": response.json()}

            elif tool_name == "create_margin_rule":
                url = f"{SCENARIO_API_BASE_URL}/api/v1/pricing-rules/rule/margin"
                response = await client.post(url, headers=headers, json=tool_args)
                response.raise_for_status()
                return {"success": True, "data": response.json()}

            elif tool_name == "create_step_rule":
                url = f"{SCENARIO_API_BASE_URL}/api/v1/pricing-rules/rule/step"
                response = await client.post(url, headers=headers, json=tool_args)
                response.raise_for_status()
                return {"success": True, "data": response.json()}

            elif tool_name == "create_price_rule":
                url = f"{SCENARIO_API_BASE_URL}/api/v1/pricing-rules/rule/price"
                response = await client.post(url, headers=headers, json=tool_args)
                response.raise_for_status()
                return {"success": True, "data": response.json()}

            elif tool_name == "create_cost_change_rule":
                url = f"{SCENARIO_API_BASE_URL}/api/v1/pricing-rules/rule/cost-change"
                response = await client.post(url, headers=headers, json=tool_args)
                response.raise_for_status()
                return {"success": True, "data": response.json()}

            elif tool_name == "delete_rule":
                rule_id = tool_args.get("rule_id")
                rule_type = tool_args.get("rule_type")

                # IMPORTANT: Always soft delete (never use hard_delete=true)
                # Add rule_type as query parameter for validation
                url = f"{SCENARIO_API_BASE_URL}/api/v1/pricing-rules/rule/{rule_id}?rule_type={rule_type}"
                response = await client.delete(url, headers=headers)
                response.raise_for_status()
                return {"success": True, "data": response.json()}

            else:
                return {"success": False, "error": f"Unknown tool: {tool_name}"}

    except httpx.HTTPStatusError as e:
        logger.error(f"Scenario API HTTP error: {e.response.status_code} - {e.response.text}")
        return {
            "success": False,
            "error": f"API returned status {e.response.status_code}: {e.response.text}"
        }
    except Exception as e:
        logger.error(f"Error executing tool {tool_name}: {str(e)}")
        return {"success": False, "error": str(e)}

# Routes
@api_router.get("/")
async def root():
    return {"message": "ClearDemand AI Pricing Analyst API"}

# Chat management
@api_router.post("/chats", response_model=Chat)
async def create_chat(input: ChatCreate):
    chat = Chat(title=input.title)
    doc = chat.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    doc['updated_at'] = doc['updated_at'].isoformat()
    await db.chats.insert_one(doc)
    return chat

@api_router.get("/chats", response_model=List[Chat])
async def get_chats():
    chats = await db.chats.find({}, {"_id": 0}).sort("updated_at", -1).to_list(100)
    for chat in chats:
        if isinstance(chat['created_at'], str):
            chat['created_at'] = datetime.fromisoformat(chat['created_at'])
        if isinstance(chat['updated_at'], str):
            chat['updated_at'] = datetime.fromisoformat(chat['updated_at'])
    return chats

@api_router.delete("/chats/{chat_id}")
async def delete_chat(chat_id: str):
    result = await db.chats.delete_one({"id": chat_id})
    await db.messages.delete_many({"chat_id": chat_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Chat not found")
    return {"message": "Chat deleted"}

# Messages
@api_router.get("/chats/{chat_id}/messages", response_model=List[Message])
async def get_messages(chat_id: str):
    messages = await db.messages.find({"chat_id": chat_id}, {"_id": 0}).sort("timestamp", 1).to_list(1000)
    for msg in messages:
        if isinstance(msg['timestamp'], str):
            msg['timestamp'] = datetime.fromisoformat(msg['timestamp'])
    return messages

@api_router.post("/chats/{chat_id}/messages")
async def send_message(chat_id: str, input: MessageCreate):
    # Save user message
    user_msg = Message(chat_id=chat_id, role="user", content=input.content)
    user_doc = user_msg.model_dump()
    user_doc['timestamp'] = user_doc['timestamp'].isoformat()
    await db.messages.insert_one(user_doc)
    
    # Get chat history for context
    messages_history = await db.messages.find({"chat_id": chat_id}, {"_id": 0}).sort("timestamp", 1).to_list(1000)
    
    # Convert MongoDB messages to format needed for Gemini API
    conversation_messages = []
    for msg in messages_history:
        conversation_messages.append({
            "role": msg["role"],
            "content": msg["content"]
        })
    
    # Add the current user message
    conversation_messages.append({
        "role": "user",
        "content": input.content
    })
    
    # Use system prompt from system_prompts.py
    system_prompt = PRICING_ANALYST_PROMPT

    # Get Gemini API key
    gemini_api_key = os.environ.get('GEMINI_API_KEY', '')

    if not gemini_api_key:
        response = DEMO_RESPONSE_TEMPLATE.format(user_message=input.content)
    else:
        # Call Gemini API
        response = await call_gemini_api(gemini_api_key, conversation_messages, system_prompt)
    
    # Save assistant message
    assistant_msg = Message(chat_id=chat_id, role="assistant", content=response)
    assistant_doc = assistant_msg.model_dump()
    assistant_doc['timestamp'] = assistant_doc['timestamp'].isoformat()
    await db.messages.insert_one(assistant_doc)
    
    # Update chat timestamp and title if first message
    chat_doc = await db.chats.find_one({"id": chat_id})
    if chat_doc:
        update_data = {"updated_at": datetime.now(timezone.utc).isoformat()}
        if chat_doc.get('title') == "New chat":
            # Generate a title from the first user message
            title = input.content[:50] + "..." if len(input.content) > 50 else input.content
            update_data['title'] = title
        await db.chats.update_one({"id": chat_id}, {"$set": update_data})
    
    return {"user_message": user_msg, "assistant_message": assistant_msg}

# Root route
@app.get("/")
async def root():
    return {
        "message": "ClearDemand AI Pricing Analyst API",
        "docs": "/docs",
        "api": "/api"
    }

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Gemini API helper function with Function Calling support
async def call_gemini_api(api_key: str, messages: List[dict], system_prompt: str) -> str:
    """
    Call Google Gemini API with function calling support
    """
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

    # Build contents array - Gemini expects array of content objects
    contents = []

    # For conversation history, we need to include previous messages
    # Format: each message is an object with "role" and "parts"
    for msg in messages:
        role = "user" if msg["role"] == "user" else "model"
        text = msg["content"]

        # Prepend system prompt to the very first user message
        if len(contents) == 0 and role == "user" and system_prompt:
            text = f"{system_prompt}\n\n{text}"

        contents.append({
            "role": role,
            "parts": [{"text": text}]
        })

    # Convert tool definitions to Gemini's format
    tools_config = [{
        "function_declarations": [
            {
                "name": tool["name"],
                "description": tool["description"],
                "parameters": tool["parameters"]
            }
            for tool in ALL_TOOLS
        ]
    }]

    payload = {
        "contents": contents,
        "tools": tools_config
    }

    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": api_key
    }

    try:
        max_iterations = 5  # Prevent infinite loops
        iteration = 0

        while iteration < max_iterations:
            iteration += 1

            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(url, json=payload, headers=headers)
                response.raise_for_status()
                result = response.json()

                if "candidates" not in result or len(result["candidates"]) == 0:
                    logger.error(f"Unexpected Gemini API response format: {result}")
                    return "I received an unexpected response format from the API."

                candidate = result["candidates"][0]
                content = candidate.get("content", {})
                parts = content.get("parts", [])

                if not parts:
                    return "I received an empty response from the AI."

                # Check if response contains function calls
                function_calls = [part for part in parts if "functionCall" in part]

                if function_calls:
                    # Execute all function calls
                    function_responses = []

                    for fc_part in function_calls:
                        func_call = fc_part["functionCall"]
                        func_name = func_call["name"]
                        func_args = func_call.get("args", {})

                        logger.info(f"Executing tool: {func_name} with args: {func_args}")

                        # Execute the tool
                        tool_result = await execute_tool_call(func_name, func_args)

                        # Build function response
                        function_responses.append({
                            "functionResponse": {
                                "name": func_name,
                                "response": {
                                    "name": func_name,
                                    "content": tool_result
                                }
                            }
                        })

                    # Add function call to conversation
                    contents.append({
                        "role": "model",
                        "parts": function_calls
                    })

                    # Add function responses to conversation
                    contents.append({
                        "role": "user",
                        "parts": function_responses
                    })

                    # Update payload with new conversation including function responses
                    payload["contents"] = contents

                    # Continue the loop to get Gemini's response with the function results
                    continue

                # No function calls - extract text response
                text_parts = [part.get("text", "") for part in parts if "text" in part]
                if text_parts:
                    return " ".join(text_parts)

                return "I couldn't generate a proper response."

        return "I reached the maximum number of function calls. Please try rephrasing your request."

    except httpx.HTTPStatusError as e:
        logger.error(f"Gemini API HTTP error: {e.response.status_code} - {e.response.text}")
        error_text = e.response.text
        if "API_KEY_INVALID" in error_text or "401" in str(e.response.status_code):
            return "Invalid API key. Please check your GEMINI_API_KEY in the .env file."
        return f"I encountered an error communicating with the AI service. Status: {e.response.status_code}"
    except Exception as e:
        logger.error(f"Error calling Gemini API: {str(e)}")
        return f"I encountered an error: {str(e)}. Please try again later."

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
