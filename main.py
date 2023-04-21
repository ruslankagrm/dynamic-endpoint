from fastapi import FastAPI
from fastapi.openapi.models import Response
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


def register_new_endpoint(name, desc, params, code, result):
    def exec_code(params):
        exec(code, globals(), locals())
        return result_model.parse_raw(result)

    result_model = type("ResultModel", (BaseModel,), result)

    @app.get(name, description=desc, response_model=result_model)
    async def dynamic_endpoint(response: Response, **query_params):
        for key, value in query_params.items():
            if key not in params or not isinstance(value, eval(params[key]["type"])):
                response.status_code = 400
                return {"detail": f"Invalid value for parameter {key}"}

        result = exec_code(query_params)
        return result.dict()
