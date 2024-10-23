import smc100_base
import time

smc1 = smc100_base.smc100(COM='COM8')
# smc1.get_errors(controller=1)
# smc1.home(controller=1)
# smc1.home(controller=2)
# smc1.get_state(controller=2)
# while True:
#     smc1.move_relative(controller=2, position=15.0)
#     time.sleep(1)
#     smc1.move_relative(controller=2, position=-15.0)
#     time.sleep(1)
# smc1.leave_DISABLE_state()
# smc1.get_state(controller=1)