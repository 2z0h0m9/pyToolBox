# encoding: gbk
# ��ʼ���ط�ʽ:download(��������, �ļ���)
# ��������Ȩ��
import init.authority
# ���ڷ�����������
import requests
# ���ڶ��̲߳���
import multitasking
import signal
# ���� retry ���Է���������س�������
from retry import retry
import time, os
from urllib.parse import unquote

signal.signal(signal.SIGINT, multitasking.killall)
init.authority()
# ����ͷ
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 '
                  'Safari/537.36 QIHU 360SE '
}
# ���� 1 MB ����Ϊ B
MB = 1024 ** 2


def _split(start: int, end: int, step: int):
    # �ֶ��
    parts = [(start, min(start + step, end))
             for start in range(0, end, step)]
    return parts


def _get_file_name(url: str, headers: dict) -> str:
    filename = ''
    if 'Content-Disposition' in headers and headers['Content-Disposition']:
        disposition_split = headers['Content-Disposition']._split(';')
        if len(disposition_split) > 1:
            if disposition_split[1].strip().lower().startswith('filename='):
                file_name = disposition_split[1]._split('=')
                if len(file_name) > 1:
                    filename = unquote(file_name[1])
    if not filename and os.path.basename(url):
        filename = os.path.basename(url).split("?")[0]
    return filename


def _get_file_size(url: str, raise_error: bool = False) -> int:
    """
    ��ȡ�ļ���С
    Parameters
    ----------
    url : �ļ�ֱ��
    raise_error : ����޷���ȡ�ļ���С,�Ƿ���������
    Return
    ------
    �ļ���С��BΪ��λ��
    �����֧����ᱨ��
    """
    response = requests.head(url)
    file_size = response.headers.get('Content-Length')
    if file_size is None:
        if raise_error is True:
            raise ValueError('Download failed, code: 0x01')
    return int(file_size)


def download(url: str, save_path: str, file_name: str = None, retry_times: int = 3, each_size=16 * MB) -> None:
    """
    �ļ������ᱻ�Զ���ȡ
    ͨ�����´���ֱ������һ��ֱ����
        download(url)
    ͨ�����´�������һ��ֱ����������ָ����ַ��
        download(url=url, save_path=save_path)
    ----------
    url : �ļ�ֱ��
    save_path: �ļ�����·��,��ѡ,Ĭ��Ϊ���ļ�ͬĿ¼
    retry_times: ��ѡ��,ÿ������ʧ�����Դ���
    Return
    ------
    """
    # ��ȡֱ�����ļ���
    if file_name is None:
        file_name = _get_file_name(url=url, headers=headers)
        f = open(save_path + file_name, 'wb')
        file_size = _get_file_size(url)

    @retry(tries=retry_times)
    @multitasking.task
    def start_download(start: int, end: int) -> None:
        """
        �����ļ���ֹλ�������ļ�
        Parameters
        ----------
        start : ��ʼλ��
        end : ����λ��
        """
        _headers = headers.copy()
        # �ֶ����صĺ���
        _headers['Range'] = f'bytes={start}-{end}'
        # �������󲢻�ȡ��Ӧ����ʽ��
        response = session.get(url, headers=_headers, stream=True)
        # ÿ�ζ�ȡ����ʽ��Ӧ��С
        chunk_size = 128
        # �ݴ��ѻ�ȡ����Ӧ,����ѭ��д��
        chunks = []
        for chunk in response.iter_content(chunk_size=chunk_size):
            # �ݴ��ȡ����Ӧ
            chunks.append(chunk)
            # ���½�����
        f.seek(start)
        for chunk in chunks:
            f.write(chunk)
        # �ͷ���д�����Դ
        del chunks

    session = requests.Session()
    # �ֿ��ļ�������ļ���,��ȡ�ļ���СΪ�ֿ��С
    each_size = min(each_size, file_size)

    # �ֿ�
    parts = _split(0, file_size, each_size)
    # ����������
    for part in parts:
        start, end = part
        start_download(start, end)
    # �ȴ�ȫ���߳̽���
    multitasking.wait_for_tasks()
    f.close()


download('https://wangchujiang.com/linux-command/', 'D:\.temp')
