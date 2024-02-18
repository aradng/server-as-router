from fastapi import FastAPI
import uvicorn
import os

app = FastAPI()


@app.get("/vpn/{state}")
async def change_state(state: str):
    if state == "on":
        # turn vpn on
        cmd = "sudo tailscale up --reset --accept-routes --advertise-routes=192.168.1.0/24 --exit-node-allow-lan-access --exit-node=100.64.0.2"
        os.system(cmd)
        return cmd
    elif state == "off":
        # turn vpn off
        cmd = "sudo tailscale up --reset --accept-routes --advertise-routes=192.168.1.0/24 --advertise-exit-node"
        os.system(cmd)
        return cmd
    else:
        return "error"


if __name__ == "__main__":
    uvicorn.run("switch-server:app", host="0.0.0.0", port=8000, log_level="info", reload=True)
