# -*- coding: utf-8 -*-
# Copyright (C) 2025-present <andrija.junzki AT gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# ---
# This file includes code migrated from DoiiarX/NLCISBNPlugin.
# Original Copyright (c) 2025 DoiiarX.
# Licensed under the Apache License, Version 2.0.
# * Modified by Andrija Junzki in 2025 to integrate into the ByK Service.

import typing as ty  # noqa: F401

import re
import urllib.request
import urllib.parse
import time
import hashlib
from random import randint
from bs4 import BeautifulSoup

from .clc_parser import Parser

# 常量定义：URL 和头信息
BASE_URL = "http://opac.nlc.cn/F"
PROVIDER_ID = "isbn"
SEARCH_URL_TEMPLATE = BASE_URL + "?func=find-b&find_code=ISB&request={isbn}&local_base=NLC01" + \
                      "&filter_code_1=WLN&filter_request_1=&filter_code_2=WYR&filter_request_2=" + \
                      "&filter_code_3=WYR&filter_request_3=&filter_code_4=WFM&filter_request_4=&filter_code_5=WSL&filter_request_5="
SEARCH_URL_TEMPLATE_TITLE = BASE_URL + "?func=find-b&find_code=WTP&request={title}&local_base=NLC01" + \
                      "&filter_code_1=WLN&filter_request_1=&filter_code_2=WYR&filter_request_2=" + \
                      "&filter_code_3=WYR&filter_request_3=&filter_code_4=WFM&filter_request_4=&filter_code_5=WSL&filter_request_5="

HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cache-Control': 'max-age=0',
    'DNT': '1',
    'Host': 'opac.nlc.cn',
    'Proxy-Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0'
}

MAX_WORKERS = 2
MAX_TITLE_LIST_NUM = 6
SPIDER_BASE_SLEEP_TIME = 200
IS_STRIP_TITLE = True
IS_STRIP_AUTHOR = True
IS_NCLHASH = True
IS_PURSETAG = False
IS_FUZZY_SEARCH_WITH_AUTHOR = True
ADD_CLC_TO_TAGS = True
CONVERT_CLC_TO_TAG = True
CLC_PARSE_LEVEL = 2

def spider_sleep():
    """
    模拟爬虫睡眠时间。(结果近似正态分布。)

    函数通过模拟掷8个120面的骰子并求和，加上一个随机数和基础睡眠时间，来确定睡眠时间，并使当前线程进入睡眠状态。
    """
    sleep_time = sum(randint(1, 120) for _ in range(8))  # 掷3个8到120面的骰子并求和
    sleep_time = sleep_time + randint(30, 600) + SPIDER_BASE_SLEEP_TIME
    time.sleep(sleep_time / 1000)


def extract_data_info(html):
    pattern = r"第\s+(\d+)\s+条记录\(共\s+(\d+)\s+条\)"
    match = re.search(pattern, html)
    if match:
        current_record, total_records = match.groups()
        return int(current_record), int(total_records)
    else:
        return None, None

def hash_utf8_string(input_string):
    # 将字符串编码为UTF-8
    encoded_string = input_string.encode('utf-8')
    
    # 使用md5算法计算哈希值
    hasher = hashlib.md5()
    hasher.update(encoded_string)
    
    # 返回十六进制格式的哈希值
    return hasher.hexdigest()

def get_dynamic_url(log):
    """
    从基础页面获取动态URL。
    :param log: 日志记录器。
    :return: 动态URL或None（获取失败时）。
    """
    
    response = urllib.request.urlopen(urllib.request.Request(BASE_URL, headers=HEADERS), timeout=10)
    response_text = response.read().decode('utf-8')
    dynamic_url_match = re.search(r"http://opac.nlc.cn:80/F/[^\s?]*", response_text)
    if dynamic_url_match:
        dynamic_url = dynamic_url_match.group(0)
        return dynamic_url
    else:
        raise ValueError("无法找到动态URL")

# def title2metadata(title, log, result_queue, clean_downloaded_metadata, max_workers=MAX_WORKERS, max_title_list_num=MAX_TITLE_LIST_NUM ):
#     if not isinstance(title, str):
#         raise TypeError("title必须是字符串")
#
#     title = urllib.parse.quote(f"{title}")
#     dynamic_url = get_dynamic_url(log)
#     if not dynamic_url:
#         return None
#
#     search_url = SEARCH_URL_TEMPLATE_TITLE.format(title=title)
#
#     response = urllib.request.urlopen(urllib.request.Request(search_url, headers=HEADERS), timeout=10)
#
#     response_text = response.read().decode('utf-8')
#
#     titlelist = parse_search_list(response_text, log)
#
#     spider_sleep()
#
#
#     if len(titlelist)>MAX_TITLE_LIST_NUM:
#         titlelist = titlelist[:MAX_TITLE_LIST_NUM]
#     # 使用线程池处理并发请求
#     metadatas = []
#     with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
#         future_to_url = {executor.submit(url2metadata, item[1], log, result_queue, clean_downloaded_metadata, max_workers= MAX_WORKERS, max_title_list_num= MAX_TITLE_LIST_NUM): item for item in titlelist}
#         for future in as_completed(future_to_url):
#             data = future.result()
#             if data:
#                 metadatas.append(data)
#     return metadatas
#
# def url2metadata(url, log, result_queue, clean_downloaded_metadata, max_workers= MAX_WORKERS, max_title_list_num= MAX_TITLE_LIST_NUM ):
#     if not isinstance(url, str):
#         raise TypeError("url必须是字符串")
#     search_url = url
#
#     spider_sleep()
#
#     try:
#         response = urllib.request.urlopen(urllib.request.Request(search_url, headers=HEADERS), timeout=10)
#         response_text = response.read().decode('utf-8')
#         metadata = to_metadata(get_parse_metadata(response_text, None, log), False, log)
#         clean_downloaded_metadata(metadata)
#         result_queue.put(metadata)
#         return metadata
#     except:
#         return None

def parse_search_list(html, log): 
    soup = BeautifulSoup(html, "html.parser")
    titlelist = []
    # 找到所有class为itemtitle的<div>元素
    itemtitle_elements = soup.find_all('div', class_='itemtitle')

    # 遍历每个匹配的元素
    for itemtitle_element in itemtitle_elements:
        # 获取文本内容
        itemtitle = itemtitle_element.get_text()
        
        # 找到链接<a>标签并获取其href属性值
        link = itemtitle_element.find('a')['href']
        titlelist.append([itemtitle,link])
    return titlelist

def canonical(isbnlike):
    """标准化ISBN，保留数字和X。"""
    numb = [c for c in isbnlike if c in '0123456789Xx']
    if numb and numb[-1] == 'x':
        numb[-1] = 'X'
    isbn = ''.join(numb)
    # 筛除特殊情况
    if (isbn and len(isbn) not in (10, 13)
            or isbn in ('0000000000', '0000000000000', '000000000X')
            or isbn.find('X') not in (9, -1) or isbn.find('x') != -1):
        return ''
    return isbn

def is_isbn10(isbn10):
    """验证ISBN-10格式"""
    isbn10 = canonical(isbn10)
    if len(isbn10) != 10:
        return False  # 校验长度是否为10
    return bool(check_digit10(isbn10[:-1]) == isbn10[-1])  # 校验位是否有效

def check_digit10(firstninedigits):
    """计算ISBN-10的校验位"""
    if len(firstninedigits) != 9:
        return ''
    try:
        int(firstninedigits)
    except ValueError:
        return ''
    val = sum((i + 2) * int(x) for i, x in enumerate(reversed(firstninedigits)))
    remainder = int(val % 11)
    if remainder == 0:
        tenthdigit = 0
    else:
        tenthdigit = 11 - remainder
    return str(tenthdigit) if tenthdigit != 10 else 'X'

def is_isbn13(isbn13):
    """验证ISBN-13格式"""
    isbn13 = canonical(isbn13)
    if len(isbn13) != 13:
        return False
    if isbn13[0:3] not in ('978', '979'):
        return False
    return bool(check_digit13(isbn13[:-1]) == isbn13[-1])

def check_digit13(firsttwelvedigits):
    """计算ISBN-13的校验位"""
    if len(firsttwelvedigits) != 12:
        return ''
    try:
        int(firsttwelvedigits)
    except ValueError:
        return ''
    val = sum((i % 2 * 2 + 1) * int(x) for i, x in enumerate(firsttwelvedigits))
    thirteenthdigit = 10 - int(val % 10)
    return str(thirteenthdigit) if thirteenthdigit != 10 else '0'

def to_isbn13(isbn10):
    """将ISBN-10转换为ISBN-13"""
    isbn10 = canonical(isbn10)  # 标准化ISBN-10
    if len(isbn10) == 13 and is_isbn13(isbn10):  # 如果已经是ISBN-13，直接返回
        return isbn10
    if not is_isbn10(isbn10):  # 如果不是有效的ISBN-10
        return ''
    isbn13 = '978' + isbn10[:-1]  # 去掉ISBN-10的最后一位，添加"978"前缀
    check = check_digit13(isbn13)  # 计算校验码
    return isbn13 + check if check else ''  # 返回完整的ISBN-13

def isbn2meta(isbn, log):
    """
    将ISBN转换为元数据。
    :param isbn: ISBN号码，作为字符串。
    :param log: 日志记录器。
    :return: 解析后的元数据或None（获取失败时）。
    """
    if not isinstance(isbn, str):
        log.info("ISBN必须是字符串")
        raise TypeError("ISBN必须是字符串")

    try:
        isbn_match = re.match(r"\d{10,}", isbn).group()
    except AttributeError:
        log.info(f"无效的ISBN代码: {isbn}")
        raise ValueError(f"无效的ISBN代码: {isbn}")

    if isbn_match != isbn:
        log.info(f"无效的ISBN代码: {isbn}")
        raise ValueError(f"无效的ISBN代码: {isbn}")

    dynamic_url = get_dynamic_url(log)
    if not dynamic_url:
        return None

    search_url = SEARCH_URL_TEMPLATE.format(isbn=isbn)
    
    response = urllib.request.urlopen(urllib.request.Request(search_url, headers=HEADERS), timeout=10)
    response_text = response.read().decode('utf-8')
    parse_metadata = get_parse_metadata(response_text, isbn, log)
    return parse_metadata

def parse_isbn(html, log):
    """
    从给定的HTML内容中解析出ISBN号。

    :param html: 包含ISBN信息的HTML文本。
    :param log: 用于记录日志信息的函数或日志记录器。
    :return: 解析出的ISBN号，如果未找到则为空字符串。
    """

    # 定义匹配ISBN的正则表达式模式
    isbn_pattern = r'ISBN: ([\d\-]+)'
    
    # 在HTML文本中搜索ISBN号的匹配项
    isbn_matches = re.search(isbn_pattern, html)

    # 如果找到匹配项，则将ISBN保存到isbn变量中，否则记录未找到的信息
    if isbn_matches:
        isbn = isbn_matches.group(1)
        isbn = isbn.replace('-','')
        if is_isbn10(isbn):
            isbn = to_isbn13(isbn)
    else:
        log.info(f'未找到ISBN号')
        isbn = ''
    
    # 记录找到的或未找到的ISBN号，并返回结果

    log.info(f'解析得到的ISBN号: {isbn}')

    return isbn


def get_parse_metadata(html, isbn, log):
    """
    从BeautifulSoup对象中解析元数据。
    :param html: html。
    :param isbn: ISBN号码，作为字符串。
    :param log: 日志记录器。
    :return: 解析后的元数据或None（解析失败时）。
    """
    web_isbn = parse_isbn(html, log)
    soup = BeautifulSoup(html, "html.parser")
    
    data = {}
    prev_td1 = ''
    prev_td2 = ''
    data.update({'isbn': isbn})
    data.update({web_isbn: web_isbn})
    
    try:
        table = soup.find("table", attrs={"id": "td"})
        if not table:
            return None
    except Exception as e:
        log.error(f"解析HTML时出错: {e}")
        return None

    tr_elements = table.find_all('tr')

    for tr in tr_elements:
        td_elements = tr.find_all('td', class_='td1')
        if len(td_elements) == 2:
            td1 = td_elements[0].get_text(strip=True).replace('\n', '').replace('\xa0', ' ')
            td2 = td_elements[1].get_text(strip=True).replace('\n', '').replace('\xa0', ' ')
            if td1 == '' and td2 == '':
                continue
            if td1:
                data.update({td1: td2.strip()})
            else:
                data.update({prev_td1: '\n'.join([prev_td2, td2]).strip()})
            prev_td1 = td1.strip()
            prev_td2 = td2.strip()
            
    # 优化标题格式
    title = data.get("题名与责任", f"{isbn}")
    if IS_STRIP_TITLE:
        pattern = r"([\u4e00-\u9fa5a-zA-Z0-9]+(?:[\u4e00-\u9fa5a-zA-Z0-9\s]+)?)(?=\s\[[\u4e00-\u9fa5]{2}\])" #
        try:
            match = re.search(pattern, title)
            if match:
                title = match.group(1)
        except re.error as e:
            log.error(f"正则表达式匹配错误: {e}, title: {title}")

    authors = data.get("著者", "").split(' & ')
    if IS_STRIP_AUTHOR:
        author_pattern = re.compile(r'^(.*?)\s+(?:著|编)')
        try:
            stripped_authors = []
            for author_entry in authors:
                match = author_pattern.match(author_entry)
                if match:
                    author_name = match.group(1)
                    stripped_authors.append(author_name)
            authors = stripped_authors
        except re.error as e:
            log.error(f"正则表达式匹配错误: {e}, authors: {authors}")

    # 使用正则表达式匹配日期
    year, month, day = '', '', ''
    # 从"通用数据"第10-13位提取出版年份
    pubdate_match = re.search(r'\d{9}(\d{4})', data.get("通用数据", ""))
    if pubdate_match:
        year = pubdate_match.group(1)
        pubdate = year  # 仅使用年份
    else:
        # 如果无法从"通用数据"提取，则从"出版项"提取年份
        pubdate_match = re.search(r'\b(\d{4})\b', data.get("出版项", ""))
        if pubdate_match:
            year = pubdate_match.group(1)
            pubdate = year  # 仅使用年份
        else:
            pubdate = ""

    publisher_match = re.search(r':\s*(.+),\s', data.get("出版项", ""))
    publisher = publisher_match.group(1) if publisher_match else ""
    
    tags = data.get("主题", "").replace('--', '&')
    if not IS_PURSETAG:
        tags += f' & {publisher}'
        if year:
            tags += f' & {year}'
        # 处理中图分类号相关选项
        clc_code = data.get("中图分类号", "")
        if ADD_CLC_TO_TAGS:
            if CONVERT_CLC_TO_TAG:
                # 使用 Parser 解析中图分类号
                parse_level = CLC_PARSE_LEVEL
                parsed_clc = Parser.parse(clc_code)
                if parsed_clc:
                        clc_codes = list(parsed_clc.values())[0]
                        if len(clc_codes) >= parse_level:
                            clc_info = Parser.get_clc_info_by_code(clc_codes[parse_level - 1])
                            if clc_info:
                                tags += f' & {clc_info["namePath"][parse_level - 1]}'
                        elif 0 < len(clc_codes) < parse_level:
                            tags += f' & {clc_codes[-1]}'
                else:
                    tags += f' & {clc_code}'
            else:
                tags += f' & {clc_code}'
    tags = [tag.strip() for tag in re.split(r'[&\s]+', tags) if tag.strip()]
    
    metadata = {
        "title": title,
        "tags": tags,
        "comments": data.get("内容提要", ""),
        'publisher': publisher,
        'pubdate': pubdate,
        'authors': authors,
        "isbn": data.get(f"{web_isbn}", f"{isbn}")
    }
    return metadata
