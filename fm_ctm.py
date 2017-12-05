# coding: utf-8
"""Freemindファイルから組み合わせデータを出力"""

import xml.etree.ElementTree as ET
import subprocess
import argparse

class TestConditionGenerator(object):
    """FreeMindファイルからテスト条件リストのファイルを出力"""

    def __init__(self):
        self._clsf_dict = {}

    def get_testcon(self):
        """因子水準の組を読み出す"""
        return self._clsf_dict

    def _get_testcon_from_node(self, parent):
        """freemindeのノードから再帰的に因子水準の組を読み出す"""

        if filter(lambda cfnode: cfnode.attrib == {'BUILTIN': 'folder'}, parent):
            # フォルダアイコン付与のノードは因子水準として抽出
            class_list = []
            for node in list(parent):
                if 'TEXT' in node.attrib:
                    class_list.append(node.attrib['TEXT'].encode('utf_8'))
            cf_text = parent.attrib['TEXT'].encode('utf_8')
            self._clsf_dict[cf_text] = class_list
        else:
            for node in list(parent):
                self._get_testcon_from_node(node)
        return self._clsf_dict

    @staticmethod
    def _print_testcondition(clsf_dict):
        """因子水準の組をインプットにpictを実行。結果を標準出力に表示"""
        # pictの実行ファイルを参照可能な場所に置くこと
        try:
            with open("temp.csv", "w") as pict_input_file:
                for key, classlist in clsf_dict.iteritems():
                    line = key + ':' + ",".join(classlist) + '\n'
                    pict_input_file.write(line)
        except IOError:
            print 'pict file cannot be created'
            raise
        subprocess.Popen("./pict temp.csv", shell=True)

    def generate_testcondition(self, input_file):
        """freemindファイルを入力に、2ワイズカバレッジ100%のテスト条件を生成・表示する"""
        try:
            cls_tree = ET.parse(input_file)
        except IOError:
            print '"%s" cannot be opened' % input_file
            raise
        except ET.ParseError:
            print '"%s" is invalid format' % input_file
            raise
        self._get_testcon_from_node(cls_tree.getroot())
        self._print_testcondition(self._clsf_dict)

def _get_parser():
    """引数パーサを返す（入力ファイル名を引数から取得）"""
    parser = argparse.ArgumentParser(
        description='This script is test tool generates test cases from freemind.')
    parser.add_argument('freemind_file', help='*.mm file', type=argparse.FileType('r'))
    return parser

def main():
    parser = _get_parser()
    tcgen = TestConditionGenerator()
    tcgen.generate_testcondition(parser.parse_args().freemind_file)

if __name__ == '__main__':
    main()
