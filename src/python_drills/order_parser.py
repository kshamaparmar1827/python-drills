from pydantic import ValidationError

from python_drills.order_models import OrderIn


def format_errors(error: ValidationError) -> list[str]:
    err_list = []
    for err in error.errors():
        location = ".".join(str(part) for part in err["loc"]) or "json"
        err_str = f"{location}: {err['msg']}"
        if err["type"] not in ["missing", "json_invalid"]:
            err_str += f" (you sent {err['input']!r})"
        err_list.append(err_str)
    return err_list


def parse_order(raw_json: str) -> OrderIn | None:
    try:
        validated_order = OrderIn.model_validate_json(raw_json)
    except ValidationError as e:
        print(f"Order rejected ({e.error_count()} problems):")
        for err_str in format_errors(e):
            print(err_str)
        return None
    else:
        return validated_order
