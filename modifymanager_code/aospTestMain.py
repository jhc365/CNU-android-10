import os

class modifyManager():#modify
    def __init__(self):
        self.code = 'testtesttest\n'

        self.imp = """import java.io.OutputStream;\nimport java.net.Socket;\nimport java.net.UnknownHostException;\n"""

        self.Zstart = """OutputStream outStream = null;\ntry{\nSocket sk = new Socket("10.0.2.2" , 8000) ;\noutStream = sk.getOutputStream();\nString startmessage = "Zend";\noutStream.write(startmessage.getBytes());\noutStream.flush();\n}catch(UnknownHostException e){\ne.printStackTrace();\n}catch (IOException e) {\ne.printStackTrace();\n}\n"""

        self.Zend = """try{\nString endmessage = "Zend";\noutStream.write(endmessage.getBytes());\noutStream.flush();\n}catch(UnknownHostException e){\ne.printStackTrace();\n}catch (IOException e) {\ne.printStackTrace();\n}\n"""
        pass

    # os.walk() 함수를 사용하면 편합니다.
    def getFilePath(self,fname):#fname 위치 찾아 문자열로 반환
        print("파일 경로 탐색을 시작합니다")
        root_dir = "./"
        for (root, dirs, files) in os.walk(root_dir):
            for walkin_fname in files:
                print(root + fname)
                if walkin_fname == fname: #일치하는 파일 발견
                    print("파일 경로를 찾았습니다")
                    return root + "/" + fname #경로 + fname으로 파일 전체 상대 경로 반환
        print("파일 경로 탐색에 실패하였습니다")
        return None #None 반환시 파일 없는것으로 판단

    # abcAfter.txt의 2번째 줄에 code를 삽입해주시면 됩니다.
    # 만약 수정이 잘못되었다면 abcBefore에서 복사해서 다시 수정하시면 됩니다.
    # ubuntu에서도 진행해보시고 실제 aosp 코드에 주석으로 코드를 삽입했을 때 권한문제가 없는지도 확인해주세요
    def modify(self,fpath): #ZygoteInit.java 파일에 소켓 통신을 통한 성능측정 코드 추가
        fpath = self.getFilePath("ZygoteInit.java")
        if fpath == None:
            print("ZygoteINit.java 파일이 존재하지 않습니다.")
            return None
        else:
            print(f'ZygoteINit.java 경로: {fpath}')

        print("ZygoteInit 코드 내 Zygote start 소켓 통신 위치 설정")
        ZstartMethod = input("코드 내 함수(문자열)을 입력하십시오 :")
        print("코드 위치를 입력하십시오")
        ZSMlocation = input("1.위 2.아래 :")

        print("ZygoteInit 코드 내 Zygote end 소켓 통신 위치 설정")
        ZendMethod = input("코드 내 함수(문자열)을 입력하십시오 :")
        print("코드 위치를 입력하십시오")
        ZEMlocation = input("1.위 2.아래 :")
        if not (((ZSMlocation == "1") | (ZSMlocation == "2"))&((ZEMlocation == "1") | (ZEMlocation == "2"))):
            print("코드 위치 선택 값이 1 또는 2가 아닙니다.")
            return

        print("zygote 코드 수정을 시작합니다")

        with open(fpath, 'r') as fr: #파일 읽기모드로 열기
            codelines = fr.readlines() #파일 읽어와 배열 저장
        fr.close()
        print("ZygoteInit 파일 열람")

        with open("ZygoteInit_backup.java",'w') as fb:#백업용 파일 생성
            for line in codelines:
                fb.write(line)#백업

        print("ZygoteInit.java 파일이 현재 폴더에 백업되었습니다.")
        fb.close()

        import_inserted = False #import문 삽입 위한 bool문

        with open(fpath, 'w') as f:
            for codeline in codelines:#읽은 파일 한줄씩 비교/ 쓰기
                if not import_inserted:
                    if "import" in codeline:
                        ###소켓 통신 위한 파일 import 추가
                        print("import문 삽입")
                        f.write(self.imp)  # 서버로 전송만을 위한 ouput 스트림
                        f.write(codeline)  # 기존 파일 코드 작성
                        import_inserted = True

                if ZstartMethod in codeline: #메인문 탐색, 메인문에에 코드 삽입
                    ### 소켓통신시작 및 Zygote 시작 알리는 통신 실시
                    print("소켓통신 시작 코드 삽입")
                    if ZSMlocation == "1":
                        f.write(self.Zstart)#소켓 연결 및 Zygote 시작 알림
                        f.write(codeline)  # 기존 파일 코드 작성
                    else:
                        f.write(codeline)  # 기존 파일 코드 작성
                        f.write(self.Zstart)  # 소켓 연결 및 Zygote 시작 알림

                if ZendMethod in codeline:#runselectloop 메소드 앞에서 zygote 종료 전송
                    print ("zygote end 통신코드 삽입")
                    if ZEMlocation == "1":
                        f.write(self.Zend)#프로세스 생성 종료 메시지
                        f.write(codeline)  # 기존 파일 코드 작성
                    else:
                        f.write(codeline)  # 기존 파일 코드 작성
                        f.write(self.Zend)  # 프로세스 생성 종료 메시지



        f.close()


        return None


class buildManager():
    def __init__(self):
        pass

    # 쉘 스크립트로 빌드하고 emulator 올리는 것까지 작성해주세요
    # 권한 문제가 없는지 확인해주세요
    def buildAOSP(self):
        return None


class performanceManager():
    def __init__(self):
        pass

    def getPID(self,packageName):
        return None

    def measureExecTime(self,pid,func):
        return None


def main():
    print('1. modifyManager')
    print('2. buildManager')
    print('3. performanceManager')
    n = input('input number to test:')

    if n == 1:
        obj = modifyManager()
    elif n == 2:
        obj = buildManager()
    elif n == 3:
        obj = performanceManager()


if __name__ == '__main__':
    main()
