#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
import urllib.parse

# 通用型分页器
class Pagination:
    def __init__(self, search_filter, items, limit, show_num_pages):
        all_pages, c = divmod(len(items), limit)
        if c > 0:
            all_pages += 1
        try:
            current_page = int(search_filter['page'])
        except:
            current_page = 1
        if current_page <= 0:
            current_page = 1
        
        # 被分页的对象，期望为数组
        self.items = items
		# 每页显示的个数
        self.limit = limit
		# 总页数
        self.all_pages = all_pages
		# 显示出来的数字页页数
        self.show_num_pages = show_num_pages
		# 当前页数
        self.current_page = current_page
		# 用于生成查询参数
        self.search = search_filter
    
    # 当前页的开始
    @property
    def start(self):
        return (self.current_page - 1) * self.limit
    
    @property
	# 当前页的结束
    def end(self):
        return self.current_page * self.limit

    # 上一页的页码
    def pre_page(self):
        if self.current_page > 1:
            self.search['page'] = self.current_page - 1
        else:
            self.search['page'] = 1
        return self.search

	# 下一页的页码
    def next_page(self):
        if self.current_page < self.all_pages:
            self.search['page'] = self.current_page + 1
        else:
            self.search['page'] = self.all_pages
        return self.search
    
    # 显示分页，用于渲染前端
    def show_pagination(self, base_url, more_arg=''):
        pages_list = []
        first_page = '<a href="%s?%s%s">首页</a>' % (base_url, urllib.parse.urlencode({'page': 1}), more_arg)
        pages_list.append(first_page)
        pre_page = '<a href="%s?%s%s">上一页</a>' % (base_url, urllib.parse.urlencode(self.pre_page()), more_arg)
        pages_list.append(pre_page)
        
        # 确认各种情况下数字页的页面范围
        if self.all_pages < self.show_num_pages:
            s = 1
            e = self.all_pages
        else:
            if self.current_page <= int(math.ceil(self.show_num_pages / 2)):
                s = 1
                e = self.show_num_pages
            else:
                if (self.current_page + 1) < self.all_pages:
                    s = self.current_page - 2
                    e = self.current_page + 2
                else:
                    s = self.current_page - 2
                    e = self.all_pages

        for p in range(s, e+1):
            if p == self.current_page:
                temp = '<a class="active" href="%s?%s%s">%s</a>' % (base_url, urllib.parse.urlencode(self.search), more_arg, p)
            else:
                self.search['page'] = p
                temp = '<a href="%s?%s%s">%s</a>' % (base_url, urllib.parse.urlencode(self.search), more_arg, p)
            pages_list.append(temp)

        next_page = '<a href="%s?%s%s">下一页</a>' % (base_url, urllib.parse.urlencode(self.next_page()), more_arg)
        pages_list.append(next_page)
        last_page = '<a href="%s?%s%s">尾页</a>' % (base_url, urllib.parse.urlencode({'page': self.all_pages}), more_arg)
        pages_list.append(last_page)
        return "".join(pages_list)
