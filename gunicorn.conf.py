# Loaded automatically by `gunicorn serve:app` from the working directory.
#
# Gunicorn's default worker timeout is 30 seconds. One /ask request can take
# longer than that on the free Gemini tier: generate.py sleeps when it has used
# 15 model calls in a minute, and sleeps again if the service returns a 429. A
# request that outlives the timeout gets its worker killed, the caller sees an
# HTML 500, and serve.py never reaches its log call, so nothing is recorded.
# 120 seconds covers the longest waits seen in the capstone trials.
#
# The worker class stays the default sync one: mcp_client.call_tool uses
# asyncio.run(), which breaks under an async worker.
timeout = 120
