import json
import os
import re
from pathlib import Path
from typing import Dict, List, Any, Optional

def snake_case(name: str) -> str:
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()

def clean_param_name(name: str) -> str:
    # Some params like 'ContentType' need to be snake_cased
    # Some might be reserved words
    if name == "from":
        return "from_idx"
    return snake_case(name).replace("-", "_")

def get_type_annotation(param_schema: Dict) -> str:
    p_type = param_schema.get("type")
    
    if p_type == "integer":
        return "int"
    elif p_type == "boolean":
        return "bool"
    elif p_type == "number":
        return "float"
    elif p_type == "array":
        return "List[Any]" # Simplification
    elif p_type == "object":
        return "Dict[str, Any]"
    else:
        return "str"

def generate_api_code(spec: Dict) -> str:
    lines = []
    lines.append("#!/usr/bin/env python")
    lines.append("# coding: utf-8")
    lines.append("")
    lines.append("import json")
    lines.append("import requests")
    lines.append("from typing import Dict, List, Optional, Any, Union")
    lines.append("from urllib.parse import urljoin")
    lines.append("")
    lines.append("class Api:")
    lines.append("    def __init__(self, base_url: str, token: Optional[str] = None, username: Optional[str] = None, password: Optional[str] = None, verify: bool = False):")
    lines.append("        self.base_url = base_url")
    lines.append("        self.token = token")
    lines.append("        self.username = username")
    lines.append("        self.password = password")
    lines.append("        self._session = requests.Session()")
    lines.append("        self._session.verify = verify")
    lines.append("        if token:")
    lines.append("            self._session.headers.update({'X-Emby-Token': token})") # Confirm header name for Jellyfin
    lines.append("        # TODO: Implement basic auth or login flow if needed")
    lines.append("")
    lines.append("    def request(self, method: str, endpoint: str, params: Dict = None, data: Dict = None, json_data: Dict = None) -> Any:")
    lines.append("        url = urljoin(self.base_url, endpoint)")
    lines.append("        response = self._session.request(method, url, params=params, data=data, json=json_data)")
    lines.append("        response.raise_for_status()")
    lines.append("        try:")
    lines.append("            return response.json()")
    lines.append("        except ValueError:")
    lines.append("            return response.text")
    lines.append("")

    for path, path_item in spec.get("paths", {}).items():
        for method, op in path_item.items():
            if method not in ["get", "post", "put", "delete", "patch"]:
                continue
            
            op_id = op.get("operationId")
            if not op_id:
                continue
            
            func_name = snake_case(op_id)
            summary = op.get("summary", "No summary")
            
            # extract params
            params = op.get("parameters", [])
            # We need to separate path params, query params, and body
            path_params_list = []
            query_params_dict = []
            
            args_required = []
            args_optional = []
            
            # Include path params in args signature
            for p in params:
                p_name = p.get("name")
                p_in = p.get("in")
                p_schema = p.get("schema", {})
                p_type = get_type_annotation(p_schema)
                clean_name = clean_param_name(p_name)
                
                if p_in == "path":
                    args_required.append(f"{clean_name}: {p_type}")
                    path_params_list.append((p_name, clean_name))
                elif p_in == "query":
                    # Make query params optional
                    args_optional.append(f"{clean_name}: Optional[{p_type}] = None")
                    query_params_dict.append((p_name, clean_name))
            
            # Check body
            request_body = op.get("requestBody")
            if request_body:
                 args_optional.append("body: Optional[Dict[str, Any]] = None")

            # Join args
            # self is always first
            all_args = ["self"] + args_required + args_optional
            args_str = ", ".join(all_args)
            
            lines.append(f"    def {func_name}({args_str}) -> Any:")
            lines.append(f"        \"\"\"{summary}\"\"\"")
            
            # Format endpoint with path params
            endpoint_str = f"\"{path}\""
            if path_params_list:
                format_args = ", ".join([f"{original}={clean}" for original, clean in path_params_list])
                endpoint_str = f"\"{path}\".format({format_args})"
                # Python format string needs {param} to match key
                # But openapi uses {param} syntax too. 
                # Let's hope the names match or used f-string if we replaced it.
                # Actually safest is to replace {name} with {name} and call format
                # But we renamed some params.
                
                # Better approach: string replacement
                lines.append(f"        endpoint = \"{path}\"")
                for original, clean in path_params_list:
                     lines.append(f"        endpoint = endpoint.replace(\"{{{original}}}\", str({clean}))")
            else:
                 lines.append(f"        endpoint = \"{path}\"")

            # Construct params dict
            if query_params_dict:
                lines.append("        params = {}")
                for original, clean in query_params_dict:
                    lines.append(f"        if {clean} is not None:")
                    lines.append(f"            params['{original}'] = {clean}")
            else:
                lines.append("        params = None")

            # Call request
            call_args = f"\"{method.upper()}\", endpoint, params=params"
            if request_body:
                call_args += ", json_data=body"
            
            lines.append(f"        return self.request({call_args})")
            lines.append("")
            
    return "\n".join(lines)


def generate_mcp_code(spec: Dict) -> str:
    lines = []
    lines.append("#!/usr/bin/env python")
    lines.append("# coding: utf-8")
    lines.append("")
    lines.append("import os")
    lines.append("from typing import Optional, List, Dict, Any")
    lines.append("from fastmcp import FastMCP, Context")
    lines.append("from pydantic import Field")
    lines.append("from jellyfin_mcp.jellyfin_api import Api")
    lines.append("from jellyfin_mcp.utils import to_boolean, to_integer")
    lines.append("")
    lines.append("mcp = FastMCP(\"jellyfin-mcp\")")
    lines.append("")
    lines.append("def get_api_client():")
    lines.append("    base_url = os.environ.get(\"JELLYFIN_BASE_URL\")")
    lines.append("    token = os.environ.get(\"JELLYFIN_TOKEN\")")
    lines.append("    username = os.environ.get(\"JELLYFIN_USERNAME\")")
    lines.append("    password = os.environ.get(\"JELLYFIN_PASSWORD\")")
    lines.append("    verify = to_boolean(os.environ.get(\"JELLYFIN_VERIFY\", \"False\"))")
    lines.append("    if not base_url:")
    lines.append("        raise ValueError(\"JELLYFIN_BASE_URL environment variable is required\")")
    lines.append("    return Api(base_url, token=token, username=username, password=password, verify=verify)")
    lines.append("")

    for path, path_item in spec.get("paths", {}).items():
        for method, op in path_item.items():
            if method not in ["get", "post", "put", "delete", "patch"]:
                continue
            
            op_id = op.get("operationId")
            if not op_id:
                continue
            
            func_name = snake_case(op_id)
            summary = op.get("summary", "No summary")
            summary = summary.replace('\n', ' ').replace('\r', '').replace('"', '\\"')
            tags = op.get("tags", ["default"])
            tag_name = tags[0] if tags else "default"
            
            lines.append(f"@mcp.tool(name=\"{func_name}\", description=\"{summary}\", tags=[\"{tag_name}\"])")
            
            # build args
            params = op.get("parameters", [])
            args_list = []
            
            # collect args for api call
            api_call_args = []
            
            args_required = []
            args_optional = []

            for p in params:
                p_name = p.get("name")
                p_in = p.get("in")
                p_schema = p.get("schema", {})
                p_type = get_type_annotation(p_schema)
                clean_name = clean_param_name(p_name)
                p_desc = p.get("description", "")
                p_desc = p_desc.replace('\n', ' ').replace('\r', '').replace('"', '\\"')
                
                # Check directly if required in param definition, defaults to False
                # But path params are always required in OpenAPI
                is_required = p.get("required", False) or p_in == "path"

                if p_in == "query":
                     # We force query params to be optional in this generator for simplicity
                     # But if it is marked required in OAS, maybe we should respect it?
                     # For now, sticking to previous logic: Query -> Optional
                     field = f"Field(default=None, description=\"{p_desc}\")"
                     lines_arg = f"{clean_name}: Optional[{p_type}] = {field}"
                     args_optional.append(lines_arg)
                else:
                     # Path params or header params (if any)
                     field = f"Field(description=\"{p_desc}\")"
                     lines_arg = f"{clean_name}: {p_type} = {field}"
                     args_required.append(lines_arg)

                api_call_args.append(f"{clean_name}={clean_name}")
            
            request_body = op.get("requestBody")
            if request_body:
                # Body is optional in our previous logic
                args_optional.append("body: Optional[Dict[str, Any]] = Field(default=None, description=\"Request body\")")
                api_call_args.append("body=body")

            func_sig = ", ".join(args_required + args_optional)
            
            lines.append(f"def {func_name}_tool({func_sig}) -> Any:")
            lines.append(f"    \"\"\"{summary}\"\"\"")
            lines.append("    api = get_api_client()")
            
            call_str = ", ".join(api_call_args)
            lines.append(f"    return api.{func_name}({call_str})")
            lines.append("")

    return "\n".join(lines)

def main():
    root = Path(__file__).parent.parent
    openapi_path = root / "openapi.json"
    
    with open(openapi_path, "r") as f:
        spec = json.load(f)
        
    api_code = generate_api_code(spec)
    api_file = root / "jellyfin_mcp" / "jellyfin_api.py"
    with open(api_file, "w") as f:
        f.write(api_code)
    print(f"Generated {api_file}")
    
    mcp_code = generate_mcp_code(spec)
    mcp_file = root / "jellyfin_mcp" / "jellyfin_mcp.py"
    with open(mcp_file, "w") as f:
        f.write(mcp_code)
    print(f"Generated {mcp_file}")

if __name__ == "__main__":
    main()
