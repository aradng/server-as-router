from fastapi import FastAPI
import os

app = FastAPI()


@app.get("/vpn/{state}")
async def change_state(state: str):
    if state == "on":
        # turn vpn on
        os.system(
            "tailscale up --reset --advertise-routes=192.168.1.0/24 --exit-node-allow-lan-access --exit-node=100.64.0.2"
        )
        return {"state": state}
    elif state == "off":
        # turn vpn off
        os.system(
            "tailscale up --reset --advertise-routes=192.168.1.0/24 --advertise-exit-node"
        )
        return {"state": state}
    else:
        return {"state": "error"}
