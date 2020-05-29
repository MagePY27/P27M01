from alvdevops0505.celery import app
import time


@app.task(name='测试任务')
def file():
    """
    测试任务：向文件写入字符串
    """
    print("111")
    t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    s = "Life is short,you need Python %s \r\n" % t
    f = open("/tmp/task.txt", 'a')
    f.write(s)
    f.close()
    return 'Test is OK'