# Synctechno SITL for GCS
 - - -
## 설치방법(Ubuntu 18.04)

- Python 및 기타 프로그램 설치
```
sudo apt-get install python-dev dos2unix python-wxgtk3.0 python-matplotlib python-opencv python-pip g++ gawk git ccache
```
- Python 라이브러리 설치
```
pip install requests
pip install paho-mqtt
pip install flask
```
- git Clone으로 가져오기
```
git clone https://bitbucket.org/synctechnoinc/ardupilot.git
```
- git submodules 초기화 및 업데이트
```
git submodule update --init --recursive
```

- ~/ardupilot/Tools/environment_install 이동, install-prereqs-ubuntu.sh 실행
```
cd ~/ardupilot/Tools/environment_install/
./install-prereqs-ubuntu.sh -y
```
> lsb_release: command not found 에러 발생시 하단 명령 입력
>```
>sudo apt-get update && sudo apt-get install -y lsb-release && sudo apt-get clean all
>```

- profile 설정
```
. ~/.profile
```
- ~/ardupilot으로 이동 후 waf 설정
```
cd ~/ardupilot
./waf clean
./waf configure --board CubeBlack
./waf copter
```
> 개발 환경에 따라 수분이 소요.
* * *
## 실행
```
sim_vehicle.py --sysid 1 --id SYNCTECHNO
```