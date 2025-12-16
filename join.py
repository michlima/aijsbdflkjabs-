import subprocess
def ping(ip):
    process = subprocess.Popen(
        ["ping","-c","4",ip],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    print("printing")
    for line in process.stdout:
        print(line,end="")
    process.wait()

