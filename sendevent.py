import os
import subprocess


# 执行命令
def runCommand(cmd):
    print("run command %s" % cmd)
    subprocess.call(cmd, shell=True)


runCommand('adb shell sendevent /dev/input/event2 1 116 1')
runCommand('adb shell sendevent /dev/input/event2 0 0 0')
runCommand('adb shell sendevent /dev/input/event2 1 116 0')
runCommand('adb shell sendevent /dev/input/event2 0 0 0')