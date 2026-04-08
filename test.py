from mavsdk import System
import asyncio

drone = System()
task_list = []
async def main(): 

    await drone.connect('udpin://0.0.0.0:14540')

    async for checks in drone.core.connection_state(): 
        if checks:
            print("successful connection")
            break 
        else:
            print("unsuccessful connection")
            continue 

    async for checks in drone.telemetry.health():
        if checks.is_global_position_ok and checks.is_home_position_ok: 
            print('successful health checkup')
            break 
        else:
            print('unsuccessful health checkup')
            continue 

    await drone.action.arm() 
    await drone.action.takeoff() 

    async for checks in drone.telemetry.in_air():
        if checks:
            print("drone is in air, starting countdown", checks)
            batteryd = asyncio.create_task(battery()) 
            coordinatesd = asyncio.create_task(coordinates())
            task_list = [batteryd, coordinatesd]

            await asyncio.sleep(30)
            break
        else:
            print("drone is not in air, can not start countdown", checks)
            continue 

    await drone.action.land() 

    async for air in drone.telemetry.in_air():
        if air:
            continue
        else:
            break 

    await drone.action.disarm()

if __name__ == "__main__":
    asyncio.run(main()) 
