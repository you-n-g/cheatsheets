#!/usr/bin/env python
#-*- coding:utf8 -*-

#pyExcelerator 的用法见 backend/django_code/views.py


# xlrd , xlwt, xlutils 的用法, 在app里中都用用法， 
# *xlwt 只支持 xls 2003*,  不支持 07!!!
# pip install xlrd xlwt xlutils

import xlrd 
read_workbook = xlrd.open_workbook(XXX_EXCEL_TEMPLATE, formatting_info=True)
read_sheet = read_workbook.sheet_by_index(0)
for rowx in xrange(read_sheet.nrows):
    for colx in xrange(read_sheet.ncols):
        read_sheet.cell_value(rowx, colx)
read_sheet.row_values(row)
read_sheet.col_values(col)

import xlwt
write_workbook = xlwt.Workbook(encoding='utf-8')
write_sheet = write_workbook.add_sheet(u'XXX_SHEET_NAME', cell_overwrite_ok=True)
write_sheet2 = write_workbook.get_sheet(0)
write_sheet.write(rowx, colx, XXX_value)
write_workbook.save(XXX_output_file)

# 拷贝 excel, 从xlrd 到 xlwt
import xlutils
from xlutils.copy import copy
write_workbook = copy(read_workbook)

# BEGIN 改变内容却不改变 样式
def _getOutCell(outSheet, rowIndex, colIndex):
    """ HACK: Extract the internal xlwt cell representation. """
    row = outSheet._Worksheet__rows.get(rowIndex)
    if not row: return None

    cell = row._Row__cells.get(colIndex)
    return cell

def setOutCell(outSheet, row, col, value):
    """ 
        Change cell value without changing formatting.
        变动内容却不改变格式
    """
    # HACK to retain cell style.
    previousCell = _getOutCell(outSheet, row, col)
    # END HACK, PART I

    outSheet.write(row, col, value)

    # HACK, PART II
    if previousCell:
        newCell = _getOutCell(outSheet, row, col)
        if newCell:
            newCell.xf_idx = previousCell.xf_idx
    # END HACK

setOutCell(XXX_write_sheet, XXX_row, XXX_col, XXX_value)
# END   改变内容却不改变 样式
