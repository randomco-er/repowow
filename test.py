from mavsdk import System
from mavsdk.offboard import PositionNedYaw
import asyncio

drone = System()
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
    print("arm")

    await drone.offboard.set_position_ned(PositionNedYaw(0.0, 0.0, 0.0, 0.0))
    print("set offboard home")

    await drone.offboard.start()
    print("start offboard")

    await drone.action.takeoff() 
    print("takeoff")

    await asyncio.sleep(5)
    print('sleep')

    print('check if 5m')
    async for coords in drone.telemetry.position_velocity_ned():
        print(-1* coords.position.down_m)
        await drone.offboard.set_position_ned(PositionNedYaw(0.0, -5.0, -1* coords.position.down_m, 0.0))
        break

    async for coords in drone.telemetry.position_velocity_ned():
        print(-1* coords.position.east_m)
        if -5.1 < -1*coords.position.east_m < -4.9:
            break
        else:
            continue
 
       

    await drone.action.land() 
    print('land')

    async for air in drone.telemetry.in_air():
        if air:
            continue
        else:
            break 

    print('disarm')

if __name__ == "__main__":
    asyncio.run(main()) 
