import requests
from typing import Literal, Any
import os
from aidbox.base import Meta, IncEx

base = os.environ.get("AIDBOX_URL")


class AidboxApi:
    @classmethod
    def api_from_id(cls, id: str, token: str):
        token = f"Bearer {token}"
        response = requests.get(url=f"{base}/fhir/{cls.__name__}/{id}", auth=token)
        response.raise_for_status()  # TODO: handle and type HTTP codes except 200+
        return cls(**response.json())

    @classmethod
    def api_bundle(cls, entry: list[Any], type: Literal["transaction"], token: str):
        token = f"Bearer {token}"
        data = {"resourceType": "Bundle", "type": type, "entry": entry}
        response = requests.post(url=f"{base}/fhir", json=data, auth=token)
        response.raise_for_status()  # TODO: handle and type HTTP codes except 200+

    @classmethod
    def api_get(cls, *args: dict[str, Any], token: str):
        token = f"Bearer {token}"
        search_params: dict[str, Any] = {}
        [search_params.update(d) for d in args]
        response = requests.get(
            url=f"{base}/fhir/{cls.__name__}", params=search_params, auth=token
        )
        response.raise_for_status()  # TODO: handle and type HTTP codes except 200+
        data = response.json()  # TODO: handle HTTP response bodies
        return (
            list(map(lambda patient: cls(**patient["resource"]), data["entry"]))
            if "entry" in data
            else []
        )

    def api_delete(self, token: str):
        token = f"Bearer {token}"
        assert self.id is not None
        resource_type = self.__class__.__name__
        response = requests.delete(
            url=f"{base}/fhir/{resource_type}/{self.id}", auth=token
        )
        response.raise_for_status()  # TODO: handle and type HTTP codes except 200+

    def api_save(self, token: str):  # create | persist | save
        token = f"Bearer {token}"
        resource_type = self.__class__.__name__
        response = requests.put(
            url=f"{base}/fhir/{resource_type}/{self.id or ''}",
            json=self.dumps(exclude_unset=True),
            auth=token,
        )
        response.raise_for_status()  # TODO: handle and type HTTP codes except 200+
        data = response.json()
        self.id = data["id"]
        self.meta = Meta(**data["meta"])

    def dumps(
        self,
        *,
        mode: Literal["json", "python"] | str = "python",
        include: IncEx = None,
        exclude: IncEx = None,
        by_alias: bool = False,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        round_trip: bool = False,
        warnings: bool = True,
    ):
        data = self.model_dump(
            mode=mode,
            by_alias=by_alias,
            include=include,
            exclude=exclude,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
            round_trip=round_trip,
            warnings=warnings,
        )

        for item in ["class", "global", "for", "import"]:
            if (item + "_") in data:
                data[item] = data[item + "_"]
                del data[item + "_"]

        return data

    @classmethod
    def api_do_request(cls, endpoint, token: str, method="GET"):
        url = f"{base}{endpoint}"
        headers = {'authorization': token}
        return requests.request(method, url, headers=headers)

    @staticmethod
    def api_open_request(endpoint, method="GET",  **kwargs):
        url = f"{base}{endpoint}"
        return requests.request(method, url, **kwargs)

