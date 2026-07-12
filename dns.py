import subprocess

for i in range(3000):
    subprocess.run(["nslookup", "google.com"])
    subprocess.run(["nslookup", "youtube.com"])
    subprocess.run(["nslookup", "naver.com"])
    subprocess.run(["nslookup", "github.com"])