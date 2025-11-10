"""
API Tool Definitions for Gemini Function Calling

This module contains all tool definitions for the Scenario API and Panel API
that are used by the Gemini AI for function calling.
"""

# Scenario API Tool Definitions
SCENARIO_TOOLS = [
    {
        "name": "list_scenarios",
        "description": "Retrieves a list of pricing scenarios. Use this when user asks about existing scenarios, wants to see all scenarios, or filter scenarios by criteria. The response contains 'items' (array of scenarios), 'page_size' (items per page), and 'total' (total count across all pages). Always check if total > items.length to inform users about more results.",
        "parameters": {
            "type": "object",
            "properties": {
                "active": {
                    "type": "boolean",
                    "description": "Filter by active status. True for active scenarios, false for inactive."
                },
                "approved": {
                    "type": "boolean",
                    "description": "Filter by approval status. True for approved scenarios."
                },
                "scenario_type": {
                    "type": "string",
                    "description": "Filter by scenario type (e.g., 'promotional', 'baseline')."
                },
                "page": {
                    "type": "integer",
                    "description": "Page number for pagination (default: 1)."
                },
                "size": {
                    "type": "integer",
                    "description": "Number of items per page (default: 50)."
                }
            }
        }
    },
    {
        "name": "get_scenario",
        "description": "Retrieves detailed information about a specific scenario by its ID. Use this when user asks about a particular scenario or wants details of a specific scenario.",
        "parameters": {
            "type": "object",
            "properties": {
                "scenario_id": {
                    "type": "integer",
                    "description": "The unique identifier of the scenario to retrieve."
                }
            },
            "required": ["scenario_id"]
        }
    },
    {
        "name": "create_scenario",
        "description": "Creates a new pricing scenario. Use this when user wants to create a new scenario. The 'name' field is mandatory. Ask user for confirmation before creating.",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The name of the scenario (required)."
                },
                "description": {
                    "type": "string",
                    "description": "Detailed description of the scenario's purpose."
                },
                "active": {
                    "type": "boolean",
                    "description": "Whether the scenario is active (default: true)."
                },
                "base_scenario": {
                    "type": "boolean",
                    "description": "Flag indicating if this is a baseline scenario."
                },
                "start_date": {
                    "type": "string",
                    "description": "Start date in ISO 8601 format (e.g., '2024-09-01T00:00:00Z')."
                },
                "end_date": {
                    "type": "string",
                    "description": "End date in ISO 8601 format (e.g., '2024-11-30T23:59:59Z')."
                },
                "target_margin": {
                    "type": "boolean",
                    "description": "Whether this scenario targets specific margin goals."
                },
                "scenario_type": {
                    "type": "string",
                    "description": "Type of scenario (e.g., 'promotional', 'baseline')."
                },
                "approved": {
                    "type": "boolean",
                    "description": "Approval status of the scenario."
                },
                "cluster_group_id": {
                    "type": "integer",
                    "description": "Reference to cluster group ID if applicable."
                }
            },
            "required": ["name"]
        }
    }
]

# Panel API Tool Definitions
PANEL_TOOLS = [
    {
        "name": "list_panels",
        "description": "Retrieves a list of pricing panels for a specific scenario with filtering options. Use this when user asks about panels in a scenario. IMPORTANT: Only scenario is required. Filters help narrow results but are optional. The API requires at least one product filter (major_department is highest priority, then department, category, sub_category, sub_sub_category OR product_group) and at least one location filter (zone_group is highest priority, then zone OR market_group). If user doesn't specify filters, ask them to provide at least major_department and zone_group to get results. Available major_departments: Enterprise, FRESH, GAS STATION, GROCERY, HARDLINES, HEALTH AND BEAUTY, HOUSEHOLD ESSENTIALS, SOFTLINES. Available zone_groups: Enterprise, Alcohol, C-store, Produce, Standard, Tobacco.",
        "parameters": {
            "type": "object",
            "properties": {
                "scenario": {
                    "type": "string",
                    "description": "Scenario name to filter panels (required)."
                },
                "panel_name": {
                    "type": "string",
                    "description": "Filter by panel name (partial match)."
                },
                "valid": {
                    "type": "boolean",
                    "description": "Filter by validation status."
                },
                "major_department": {
                    "type": "string",
                    "description": "Major department name (HIGHEST PRIORITY in product hierarchy). Options: Enterprise, FRESH, GAS STATION, GROCERY, HARDLINES, HEALTH AND BEAUTY, HOUSEHOLD ESSENTIALS, SOFTLINES."
                },
                "department": {
                    "type": "string",
                    "description": "Department name for product hierarchy filter (lower priority than major_department)."
                },
                "category": {
                    "type": "string",
                    "description": "Category name for product hierarchy filter (lower priority than department)."
                },
                "sub_category": {
                    "type": "string",
                    "description": "Sub-category name for product hierarchy filter (lower priority than category)."
                },
                "sub_sub_category": {
                    "type": "string",
                    "description": "Sub-sub-category name for product hierarchy filter (lower priority than sub_category)."
                },
                "product_group": {
                    "type": "string",
                    "description": "Product group name filter (alternative to hierarchy filters)."
                },
                "product_source": {
                    "type": "string",
                    "description": "Product group source type (required if using product_group)."
                },
                "zone_group": {
                    "type": "string",
                    "description": "Zone group name (HIGHEST PRIORITY in location hierarchy). Options: Enterprise, Alcohol, C-store, Produce, Standard, Tobacco."
                },
                "zone": {
                    "type": "string",
                    "description": "Zone name for location hierarchy filter (lower priority than zone_group)."
                },
                "location_hierarchy_id": {
                    "type": "integer",
                    "description": "Location hierarchy ID (1 for default)."
                },
                "market_group": {
                    "type": "string",
                    "description": "Market/location group name (alternative to hierarchy filters)."
                },
                "market_source": {
                    "type": "string",
                    "description": "Market group source type (required if using market_group)."
                },
                "price_type": {
                    "type": "string",
                    "description": "Price type name filter."
                },
                "rule_type": {
                    "type": "string",
                    "description": "Rule type name filter."
                },
                "rule_sub_type": {
                    "type": "string",
                    "description": "Rule sub-type name filter."
                },
                "page": {
                    "type": "integer",
                    "description": "Page number for pagination (default: 1)."
                },
                "size": {
                    "type": "integer",
                    "description": "Number of items per page (default: 10)."
                },
                "sort": {
                    "type": "string",
                    "description": "Sorting format: 'field:direction' (e.g., 'Priority:asc')."
                }
            },
            "required": ["scenario"]
        }
    },
    {
        "name": "get_panel",
        "description": "Retrieves detailed information about a specific panel by its ID. Use this when user asks about a particular panel. Don't ask user for panel ID - first list panels to find it.",
        "parameters": {
            "type": "object",
            "properties": {
                "panel_id": {
                    "type": "integer",
                    "description": "The unique identifier of the panel to retrieve."
                }
            },
            "required": ["panel_id"]
        }
    },
    {
        "name": "create_panel",
        "description": "Creates a new pricing panel. IMPORTANT: Before creating, MUST verify the scenario exists using get_scenario. If scenario doesn't exist, ask user to create it first. Requires user confirmation before creation. At least one product filter (product_node OR product_group) and one location filter (location_node OR location_group) are required.",
        "parameters": {
            "type": "object",
            "properties": {
                "scenario_id": {
                    "type": "integer",
                    "description": "Scenario ID this panel belongs to (required). MUST validate this scenario exists first."
                },
                "panel_name": {
                    "type": "string",
                    "description": "Name of the panel (required)."
                },
                "priority": {
                    "type": "integer",
                    "description": "Priority order - lower value = higher priority (required)."
                },
                "product_node": {
                    "type": "string",
                    "description": "Product hierarchy node name (department, category, etc.). Use this OR product_group."
                },
                "product_group": {
                    "type": "string",
                    "description": "Product group name. Use this OR product_node. Requires product_source if used."
                },
                "product_source": {
                    "type": "string",
                    "description": "Product group source type (required if using product_group)."
                },
                "location_node": {
                    "type": "string",
                    "description": "Location hierarchy node name (zone, zone group, etc.). Use this OR location_group."
                },
                "location_group": {
                    "type": "string",
                    "description": "Location/market group name. Use this OR location_node. Requires market_source if used."
                },
                "market_source": {
                    "type": "string",
                    "description": "Market group source type (required if using location_group)."
                },
                "comment": {
                    "type": "string",
                    "description": "Description or notes about the panel."
                },
                "hard_rule_flag": {
                    "type": "boolean",
                    "description": "Whether panel contains hard rules (default: false)."
                }
            },
            "required": ["scenario_id", "panel_name", "priority"]
        }
    },
    {
        "name": "update_panel",
        "description": "Updates an existing panel's name, priority, or comment. IMPORTANT: Only panel_name, priority, and comment can be modified. Product/location dimensions cannot be changed. Requires user confirmation before updating.",
        "parameters": {
            "type": "object",
            "properties": {
                "panel_id": {
                    "type": "integer",
                    "description": "The unique identifier of the panel to update (required)."
                },
                "scenario_id": {
                    "type": "integer",
                    "description": "Scenario ID for verification (required)."
                },
                "product_node": {
                    "type": "string",
                    "description": "Product hierarchy node for verification (if panel uses it)."
                },
                "product_group_name": {
                    "type": "string",
                    "description": "Product group name for verification (if panel uses it)."
                },
                "product_source": {
                    "type": "string",
                    "description": "Product source for verification."
                },
                "location_node": {
                    "type": "string",
                    "description": "Location hierarchy node for verification (if panel uses it)."
                },
                "location_group_name": {
                    "type": "string",
                    "description": "Location group name for verification (if panel uses it)."
                },
                "market_source": {
                    "type": "string",
                    "description": "Market source for verification."
                },
                "panel_name": {
                    "type": "string",
                    "description": "Updated panel name (optional - only include if updating)."
                },
                "priority": {
                    "type": "integer",
                    "description": "Updated priority value (optional - only include if updating)."
                },
                "comment": {
                    "type": "string",
                    "description": "Updated comment/description (optional - only include if updating)."
                }
            },
            "required": ["panel_id", "scenario_id"]
        }
    },
    {
        "name": "delete_panel",
        "description": "Soft deletes a pricing panel (panel is marked as deleted but preserved). IMPORTANT: This is always a soft delete. Requires user confirmation before deletion.",
        "parameters": {
            "type": "object",
            "properties": {
                "panel_id": {
                    "type": "integer",
                    "description": "The unique identifier of the panel to delete (required)."
                }
            },
            "required": ["panel_id"]
        }
    },
    {
        "name": "list_panel_rules",
        "description": "Retrieves all pricing rules associated with a specific panel. Use this when user asks about rules within a panel.",
        "parameters": {
            "type": "object",
            "properties": {
                "panel_id": {
                    "type": "integer",
                    "description": "The unique identifier of the panel (required)."
                },
                "page": {
                    "type": "integer",
                    "description": "Page number for pagination (default: 1)."
                },
                "size": {
                    "type": "integer",
                    "description": "Number of items per page (default: 10)."
                },
                "order_by": {
                    "type": "string",
                    "description": "Field to sort by (default: 'HardRuleRank'). Options: HardRuleRank, RuleId, Active, PriceTypeId, RuleTypeId, Valid."
                },
                "sort_order": {
                    "type": "integer",
                    "description": "Sort direction: 0 = ASC, 1 = DESC (default: 0)."
                }
            },
            "required": ["panel_id"]
        }
    }
]

# Rule API Tool Definitions
RULE_TOOLS = [
    {
        "name": "create_cpi_rule",
        "description": "Creates one or more CPI (Competitive Price Index) rules for a panel. IMPORTANT: Must validate panel exists before creating. CPI rules can be created on both hard and soft panels. Can create multiple CPI rules in a single request. Requires user confirmation.",
        "parameters": {
            "type": "object",
            "properties": {
                "panel_id": {
                    "type": "integer",
                    "description": "Panel ID to attach rules to (required). Must validate this panel exists first."
                },
                "rules": {
                    "type": "array",
                    "description": "Array of CPI rule objects. Can create multiple rules in one request.",
                    "items": {
                        "type": "object",
                        "properties": {
                            "competitor": {
                                "type": "string",
                                "description": "Competitor name (required). Must be valid in the system."
                            },
                            "rule_desc": {
                                "type": "string",
                                "description": "Rule description (required, max 150 chars)."
                            },
                            "days_until_alert": {
                                "type": "integer",
                                "description": "Days until price alert (required, >= 0)."
                            },
                            "intel_rule": {
                                "type": "boolean",
                                "description": "Whether this is an intelligent rule (default: false)."
                            },
                            "weight": {
                                "type": "number",
                                "description": "Rule weight (required for soft rule panels)."
                            },
                            "rank": {
                                "type": "integer",
                                "description": "Priority rank (required for hard rule panels)."
                            },
                            "target_cpi": {
                                "type": "number",
                                "description": "Target competitive price index."
                            },
                            "min_cpi": {
                                "type": "number",
                                "description": "Minimum CPI boundary (must be <= target_cpi)."
                            },
                            "max_cpi": {
                                "type": "number",
                                "description": "Maximum CPI boundary (must be >= target_cpi)."
                            },
                            "min_add": {
                                "type": "number",
                                "description": "Minimum additive amount (must be <= max_add)."
                            },
                            "max_add": {
                                "type": "number",
                                "description": "Maximum additive amount (must be >= min_add)."
                            },
                            "price_type": {
                                "type": "string",
                                "description": "Type of price to match: 'regular', 'promotional', or 'blended'."
                            },
                            "snap_price_point": {
                                "type": "string",
                                "description": "Price rounding direction: 'up' or 'down'."
                            },
                            "half_life_period": {
                                "type": "integer",
                                "description": "Half-life decay period (required if intel_rule=true, >= 0)."
                            },
                            "half_life_unit": {
                                "type": "string",
                                "description": "Half-life unit: 'day', 'days', 'week', or 'weeks' (required if intel_rule=true)."
                            },
                            "modal_index": {
                                "type": "integer",
                                "description": "Modal pricing index (default: 0)."
                            }
                        },
                        "required": ["competitor", "rule_desc", "days_until_alert"]
                    }
                }
            },
            "required": ["panel_id", "rules"]
        }
    },
    {
        "name": "create_margin_rule",
        "description": "Creates a margin-based pricing rule for a panel. IMPORTANT: Must validate panel exists AND is a hard rule panel (not soft). Only ONE margin rule per request. Requires user confirmation.",
        "parameters": {
            "type": "object",
            "properties": {
                "panel_id": {
                    "type": "integer",
                    "description": "Panel ID to attach rule to (required). Must validate panel exists and is a hard rule panel."
                },
                "rules": {
                    "type": "array",
                    "description": "Array with exactly ONE margin rule object.",
                    "items": {
                        "type": "object",
                        "properties": {
                            "rule_desc": {
                                "type": "string",
                                "description": "Rule description (required, max 150 chars)."
                            },
                            "target_margin": {
                                "type": "number",
                                "description": "Target profit margin 0-1 (e.g., 0.30 = 30%)."
                            },
                            "min_margin": {
                                "type": "number",
                                "description": "Minimum margin boundary 0-1 (must be <= target_margin)."
                            },
                            "max_margin": {
                                "type": "number",
                                "description": "Maximum margin boundary 0-1 (must be >= target_margin)."
                            },
                            "min_add": {
                                "type": "number",
                                "description": "Minimum additive price adjustment (must be <= max_add)."
                            },
                            "max_add": {
                                "type": "number",
                                "description": "Maximum additive price adjustment (must be >= min_add)."
                            },
                            "snap_price_point": {
                                "type": "string",
                                "description": "Price rounding direction: 'up' or 'down'."
                            }
                        },
                        "required": ["rule_desc"]
                    }
                }
            },
            "required": ["panel_id", "rules"]
        }
    },
    {
        "name": "create_step_rule",
        "description": "Creates a step-based pricing rule for a panel. IMPORTANT: Must validate panel exists AND is a hard rule panel (not soft). Only ONE step rule per request. Requires user confirmation.",
        "parameters": {
            "type": "object",
            "properties": {
                "panel_id": {
                    "type": "integer",
                    "description": "Panel ID to attach rule to (required). Must validate panel exists and is a hard rule panel."
                },
                "rules": {
                    "type": "array",
                    "description": "Array with exactly ONE step rule object.",
                    "items": {
                        "type": "object",
                        "properties": {
                            "rule_desc": {
                                "type": "string",
                                "description": "Rule description (required, max 150 chars)."
                            },
                            "max_factor": {
                                "type": "number",
                                "description": "Maximum multiplicative factor (0-999999.999999)."
                            },
                            "min_factor": {
                                "type": "number",
                                "description": "Minimum multiplicative factor (0-999999.999999, must be <= max_factor)."
                            },
                            "add_min": {
                                "type": "number",
                                "description": "Minimum additive amount (0-999999.999999, must be <= add_max)."
                            },
                            "add_max": {
                                "type": "number",
                                "description": "Maximum additive amount (0-999999.999999, must be >= add_min)."
                            }
                        },
                        "required": ["rule_desc"]
                    }
                }
            },
            "required": ["panel_id", "rules"]
        }
    },
    {
        "name": "create_price_rule",
        "description": "Creates an absolute or variable-based price rule for a panel. IMPORTANT: Must validate panel exists AND is a hard rule panel (not soft). Only ONE price rule per request. Supports price variables like [EDLP], [MAP], [MaxProfit], etc. Requires user confirmation.",
        "parameters": {
            "type": "object",
            "properties": {
                "panel_id": {
                    "type": "integer",
                    "description": "Panel ID to attach rule to (required). Must validate panel exists and is a hard rule panel."
                },
                "rules": {
                    "type": "array",
                    "description": "Array with exactly ONE price rule object.",
                    "items": {
                        "type": "object",
                        "properties": {
                            "rule_desc": {
                                "type": "string",
                                "description": "Rule description (required, max 150 chars)."
                            },
                            "target": {
                                "type": "string",
                                "description": "Target price - can be numeric (e.g., '19.99') or variable (e.g., '[EDLP]', '[MAP]', '[MaxProfit]')."
                            },
                            "min_amount": {
                                "type": "string",
                                "description": "Minimum price boundary - can be numeric or variable (must be <= target if both numeric)."
                            },
                            "max_amount": {
                                "type": "string",
                                "description": "Maximum price boundary - can be numeric or variable (must be >= target if both numeric)."
                            },
                            "snap_price_point": {
                                "type": "string",
                                "description": "Price rounding direction: 'up' or 'down'."
                            }
                        },
                        "required": ["rule_desc"]
                    }
                }
            },
            "required": ["panel_id", "rules"]
        }
    },
    {
        "name": "create_cost_change_rule",
        "description": "Creates a cost change-based pricing rule for a panel. IMPORTANT: Must validate panel exists AND is a hard rule panel (not soft). Only ONE cost change rule per request. Automatically adjusts prices when future costs change. Requires user confirmation.",
        "parameters": {
            "type": "object",
            "properties": {
                "panel_id": {
                    "type": "integer",
                    "description": "Panel ID to attach rule to (required). Must validate panel exists and is a hard rule panel."
                },
                "rules": {
                    "type": "array",
                    "description": "Array with exactly ONE cost change rule object.",
                    "items": {
                        "type": "object",
                        "properties": {
                            "rule_desc": {
                                "type": "string",
                                "description": "Rule description (required, max 150 chars)."
                            },
                            "future_window_days": {
                                "type": "integer",
                                "description": "Days into future to check cost changes (required, 0-10000)."
                            },
                            "cost_change_up": {
                                "type": "number",
                                "description": "Cost increase % threshold (0-100, e.g., 10 = 10%)."
                            },
                            "cost_change_down": {
                                "type": "number",
                                "description": "Cost decrease % threshold (0-100, e.g., 5 = 5%)."
                            },
                            "margin_change_up": {
                                "type": "integer",
                                "description": "Margin change for cost increases in basis points (0-10000, 100 bp = 1%)."
                            },
                            "margin_change_down": {
                                "type": "integer",
                                "description": "Margin change for cost decreases in basis points (0-10000)."
                            }
                        },
                        "required": ["rule_desc", "future_window_days"]
                    }
                }
            },
            "required": ["panel_id", "rules"]
        }
    },
    {
        "name": "delete_rule",
        "description": "Soft deletes a pricing rule (sets Active = 0 but preserves data). IMPORTANT: This is always a soft delete. Requires user confirmation and rule_type parameter for validation.",
        "parameters": {
            "type": "object",
            "properties": {
                "rule_id": {
                    "type": "integer",
                    "description": "The unique identifier of the rule to delete (required)."
                },
                "rule_type": {
                    "type": "string",
                    "description": "Type of rule being deleted: 'cpi', 'margin', 'step', 'price', or 'cost-change' (required for validation)."
                }
            },
            "required": ["rule_id", "rule_type"]
        }
    }
]

# Combined tools list - all available tools
ALL_TOOLS = SCENARIO_TOOLS + PANEL_TOOLS + RULE_TOOLS
