# coding = utf-8

from taskinterface import taskinterface
from PyQt6.QtWidgets import QFileDialog
import jieba.posseg as pseg
from jieba import DEFAULT_DICT_NAME
from pandas.core.internals.managers import create_block_manager_from_arrays
from pyecharts import options as opts
from pyecharts.charts import Graph

import pandas as pd
import const
import codecs
import os
import json
from tqdm import tqdm
import const

const.EXCEL_FILE = "graph_data.xlsx"
const.SHEET_NAME = "name"
const.SHEET_LINK = "link"
const.BOOKGRAPH_NAME = 'book graph'

const.BOOK_hongloumeng = '红楼梦'
const.BOOK_feihuwaizhuan = '飞狐外传'
const.BOOK_xueshanfeihu = '雪山飞狐'
const.BOOK_lianchengjue = '连城诀'
const.BOOK_tianlongbabu = '天龙八部'
const.BOOK_shediaoyingxiongzhuan = '射雕英雄传'
const.BOOK_baimaxiaoxifeng = '白马啸西风'
const.BOOK_ludingji = '鹿鼎记'
const.BOOK_xiaoaojianghu = '笑傲江湖'
const.BOOK_shujianenchoulu = '书剑恩仇录'
const.BOOK_shendiaoxialv = '神雕侠侣'
const.BOOK_xiakexing = '侠客行'
const.BOOK_yitiantulongji = '倚天屠龙记'
const.BOOK_bixuejian = '碧血剑'
const.BOOK_yuanyangjian = '鸳鸯刀'


class checkname:

    def __init__(self):
        self.checkfunc = self.check_hongloumeng_name
    
    def _fupdatefunc(self, sname: str) -> None:
        if const.BOOK_hongloumeng in sname:
            self.checkfunc = self.check_hongloumeng_name
        elif const.BOOK_feihuwaizhuan in sname:
            self.checkfunc = self.check_feihuwaizhuan_name
        elif const.BOOK_xueshanfeihu in sname:
            self.checkfunc = self.check_xueshanfeihu_name
        elif const.BOOK_lianchengjue in sname:
            self.checkfunc = self.check_lianchengjue_name
        elif const.BOOK_tianlongbabu in sname:
            self.checkfunc = self.check_tianlongbabu_name
        elif const.BOOK_shediaoyingxiongzhuan in sname:
            self.checkfunc = self.check_shediaoyingxiongzhuan_name
        elif const.BOOK_baimaxiaoxifeng in sname:
            self.checkfunc = self.check_baimaxiaoxifeng_name
        elif const.BOOK_ludingji in sname:
            self.checkfunc = self.check_ludingji_name
        elif const.BOOK_xiaoaojianghu in sname:
            self.checkfunc = self.check_xiaoaojianghu_name
        elif const.BOOK_shujianenchoulu in sname:
            self.checkfunc = self.check_shujianenchoulu_name
        elif const.BOOK_shendiaoxialv in sname:
            self.checkfunc = self.check_shendiaoxialv_name
        elif const.BOOK_xiakexing in sname:
            self.checkfunc = self.check_xiakexing_name
        elif const.BOOK_yitiantulongji in sname:
            self.checkfunc = self.check_yitiantulongji_name
        elif const.BOOK_bixuejian in sname:
            self.checkfunc = self.check_bixuejian_name
        elif const.BOOK_yuanyangjian in sname:
            self.checkfunc = self.check_yuanyangdao_name

    #检测红楼梦人名
    # 参数：待检测人名
    # 返回值：更正的人名
    def check_hongloumeng_name(self,sname : str) -> str:
        excludes = ['明白', '言语', '和尚', '小姐', '那丫头',
                    '那婆子', '老嬷嬷', '从小儿', '王爷', '何曾', '贾府', '金陵', '祖宗', '宁荣'
                    '荣国府', '梅花', '安静', '张罗', '孙子', '宁府', '桂花', '薛家', '贾家', '甄家', '那玉', '水月庵', '贾母房', '齐全',
                    '谢恩', '老先生', '道谢', '相公', '陈设', '小燕', '莫若', '听宝玉', '齐备', '明白人', '小太监', '胡闹', '水溶', '宝贝',
                    '宗祠', '天亮', '子孙', '荣府', '但凡', '古董', '青埂峰', '那道人', '钱粮', '孙女儿', '天恩', '贾府中', '殷勤', '清香',
                    '呼唤', '庄子', '老世翁', '阎王', '荣宁', '贺喜', '通灵', '云云', '宁可', '金玉', '帕子', '王府', '和睦', '宁荣二', '乐一乐',
                    '任凭', '谢礼', '寻思', '白石', '言少述', '肯依', '别提', '冷笑', '玉微微', '蒙圣恩', '邢王二', '小丫头', '荣国府',
                    '凤凰', '祖母'
                    ]
        primname1 = ['贾宝玉', '贾母', '王熙凤', '林黛玉', '薛宝钗', '王夫人', '贾政', '贾琏', '薛姨妈', '贾探春', '紫鹃', '贾珍', '尤氏', '邢夫人',
                    '薛蟠', '贾蓉', '贾芸', '周瑞家', '贾惜春', '贾环', '贾迎春', '林之孝', '赵姨娘', '夏金桂', '雪雁', '妙玉', '薛宝琴', '史湘云',
                    '巧姐', '尤二姐', '秦钟', '贾雨村', '贾兰', '平儿', '甄士隐', '秋纹', '秦氏', '司棋', '冯紫英', '红玉', '贾瑞', '包勇', '北静王',
                    '玉钏儿', '贾元春', '金钏儿', '贾元春', '甄宝玉', '尤三姐', '周瑞', '贾芹', '张华', '旺儿', '金荣', '赖大', '倪二', '李贵',
                    '贾蔷', '蒋玉菡', '鲍二', '王善保', '李十儿', '秋桐', '王子腾', '贾代儒', '马道婆', '张道士', '王太医', '李氏', '柳湘莲',
                    '邢岫烟', '李纹', '小红', '邢大舅', '李宫裁', '尤老娘', '王一贴', '李婶娘', '佩凤', '翠墨', '吴新登', '赵嬷嬷', '赵堂官',
                    '周全', '太妃', '赖尚荣', '春燕', '英莲', '林如海', '贾菌', '周姨娘', '赖嬷嬷', '俞禄', '贾敬', '石青'
                    ]

        primname = [
            '贾母',
            #十二金钗．
            '林黛玉', '薛宝钗', '贾元春', '贾迎春', '贾探春', '贾惜春', '李纨', '妙玉', '史湘云', '王熙风', '贾巧姐', '秦可卿',
            #十二丫环．
            '晴雯', '麝月', '袭人', '鸳鸯', '雪雁', '紫鹃', '碧痕', '平儿', '香菱', '金钏', '司棋', '抱琴',
            #十二家人：
            '赖大', '隹大', '王善保', '周瑞', '林之孝', '乌进孝', '包勇', '吴贵', '吴新登', '邓好时', '王柱儿', '余信',
            #十二儿 ：
            '庆儿', '昭儿', '兴儿', '隆儿', '坠儿', '喜儿', '寿儿', '丰儿', '住儿', '小舍儿', '李十儿', '玉柱儿',
            #十二贾氏：
            '贾敬', '贾赦', '贾政', '贾宝玉', '贾琏', '贾珍', '贾环', '贾蓉', '贾兰', '贾芸', '贾蔷', '贾芹',
            #十二官：
            '琪官', '芳官', '藕官', '蕊官', '药官', '玉官', '宝官', '龄官', '茄官', '艾官', '豆官', '葵官',
            #七彩．
            '彩屏', '彩儿', '彩凤', '彩霞', '彩鸾', '彩明', '彩云',
            #七尼．
            '妙玉', '智能', '智通', '智善', '圆信', '大色空', '净虚',
            #四春：
            '贾元春', '贾迎春', '贾探春', '贾惜春',
            #四宝：
            '贾宝玉', '甄宝玉', '薛宝钗', '薛宝琴',
            #四薛：
            '薛蟠', '薛蝌', '薛宝钗', '薛宝琴',
            #四王．
            '王夫人', '王熙风', '王子腾', '王仁',
            #四尤：
            '尤老娘', '尤氏', '尤二姐', '尤三姐',
            #四草辈：
            '贾蓉', '贾兰', '贾芸', '贾芹',
            #四玉辈：
            '贾胗', '贾琏', '贾环', '贾瑞',
            #四文辈：
            '贾敬', '贾赦', '贾政', '贾敏',
            #四代辈：
            '贾代儒', '贾代化', '贾代修', '贾代善',
            #四烈婢：
            '晴雯', '金钏', '鸳鸯', '司棋',
            #四清客
            '詹光', '单聘仁', '程日兴', '王作梅',
            #四无辜：
            '石呆子', '张华', '冯渊', '张金哥',
            #四小厮：
            '茗烟', '扫红', '锄药', '伴鹤',
            #四小：
            '小鹊', '小红', '小蝉', '小舍儿',
            #四婆子：
            '刘姥姥', '马道婆', '宋嬷嬷', '张妈妈',
            #四情友：
            '秦钟', '蒋玉菡', '柳湘莲', '东平王',
            #四壮客
            '乌进孝', '冷子兴', '山子野', '方椿',
            #四宦官
            '载权', '夏秉忠', '周太监', '裘世安',
            #文房四宝：
            '抱琴', '司棋', '侍画', '入画',
            #四珍宝：
            '珍珠', '琥珀', '玻璃', '翡翠',
            #一主三仆：
            '史湘云', '翠缕', '笑儿', '篆儿',
            '贾探春', '侍画', '翠墨', '小蝉',
            '贾宝玉', '茗烟', '袭人', '晴雯',
            '林黛玉', '紫鹃', '雪雁', '春纤',
            '贾惜春', '入画', '彩屏', '彩儿',
            '贾迎春', '彩风', '彩云', '彩霞'
        ]

        primname += primname1
        primname = list(set(primname))  # 去重

        #红楼梦
        if sname == '宝玉' or sname == '宝二爷' or sname == '宝兄弟' or sname == '那宝玉' or \
            sname == '向宝玉' or sname == '问宝玉' or sname == '贾琏宝玉':
            sname = '贾宝玉'
        elif sname == '凤姐' or sname == '凤姐儿' or sname == '凤丫头' or sname == '凤姐姐' or \
            sname == '那凤姐' or sname == '熙凤亲'or sname == '熙凤道' or sname=='凤姐忙':
            sname = '王熙凤'
        elif sname == '黛玉' or sname == '林姑娘' or sname == '黛玉忙' or sname == '林丫头' or \
            sname == '那黛玉' or sname == '向黛玉' or sname == '林姐姐' or sname == '林妹妹' or \
                sname == '黛玉笑' or sname == '黛玉方':
            sname = '林黛玉'
        elif sname == '宝钗' or sname == '宝钗笑' or sname == '宝丫头' or sname == '宝钗见' or \
            sname == '宝钗忙' or sname == '宝钗因' or sname == '向宝钗' or sname == '玉宝钗' or \
                sname == '宝妹妹' or sname == '宝姐姐' or sname == '宝钗素' or sname == '和宝钗' or sname == '时宝钗':
            sname = '薛宝钗'
        elif sname == '老太太' or sname == '贾母笑' or sname == '老祖宗' or sname == '贾母王' or \
            sname == '贾母因' or sname == '贾母忙' or sname == '贾母命' or sname == '贾母问' or \
                sname == '明贾母' or sname == '贾母喜' or sname == '贾母正' or sname == '贾母方' or sname == '贾母才':
            sname = '贾母'
        elif sname == '巧姐儿':
            sname = '巧姐'
        elif sname == '云儿':
            sname = '史湘云'
        elif sname == '元妃' or sname == '贾妃':
            sname = '贾元春'
        elif sname == '平儿忙' or sname == '向平儿' or sname == '平儿见' or sname == '平姐姐' or sname == '平儿拿':
            sname = '平儿'
        elif sname == '贾政道' or sname == '贾政笑' or sname == '贾政又' or sname == '贾政便' or \
            sname == '贾政回' or sname == '贾政因' or sname == '贾政忙' or sname == '贾政进' or sname == \
                '贾政听' or sname == '贾政正' or sname == '贾政叹' or sname == '贾政喝' or sname == '贾政叫' or sname == '贾政问':
            sname = '贾政'
        elif sname == '雨村':
            sname = '贾雨村'
        elif sname == '薛蟠见' or sname=='薛蟠笑':
            sname = '薛蟠'
        elif sname == '士隐':
            sname = '甄士隐'
        elif sname == '尤氏笑':
            sname = '尤氏'
        elif sname == '贾芸道' or sname == '贾芸笑':
            sname = '贾芸'
        elif sname == '雪雁道':
            sname = '雪雁'
        elif sname == '代儒':
            sname = '贾代儒'
        elif sname == '贾琏便' or sname == '贾琏忙' or sname=='贾琏贾':
            sname = '贾琏'
        elif sname == '贾珍笑' or sname == '贾珍忙' or sname == '贾珍便' or sname == '贾珍先':
            sname = '贾珍'
        elif sname == '贾环贾' or sname == '贾环见' or sname == '贾环便':
            sname = '贾环'
        elif sname == '贾蔷道':
            sname = '贾蔷'
        elif sname == '邢姑娘' or sname=='邢妹妹':
            sname = '邢岫烟'
        elif sname == '贾蓉之' or sname=='贾蓉忙':
            sname = '贾蓉'
        elif sname == '薛大爷':
            sname = '薛蟠'
        elif sname == '兰哥儿' or sname == '兰儿':
            sname = '贾兰'
        elif sname == '那秦钟' or sname == '秦钟趁' or sname == '秦钟笑':
            sname = '秦钟'
        elif sname == '秋纹笑':
            sname = '秋纹'
        elif sname == '探春':
            sname = '贾探春'
        elif sname == '迎春':
            sname = '贾迎春'
        elif sname == '惜春':
            sname = '贾惜春'
        elif sname == '金桂':
            sname = '夏金桂'
        elif sname == '宝琴':
            sname = '薛宝琴'
        elif sname == '那紫鹃':
            sname = '紫鹃'

        if sname in primname:
            return sname

        return None

    #检测飞狐外传人名
    # 参数：待检测人名
    # 返回值：更正的人名
    def check_feihuwaizhuan_name(self, sname: str) -> str:
        #《飞狐外传》人物（共有112人）
        primname = [
            '马行空','马春花','徐铮','商宝震','何思豪','阎基','田归农','苗人凤','南仁通','补锅匠','脚夫','车夫','蒋调侯',
            '店伴','钟兆文','钟兆英','钟兆能','南兰','苗若兰','商老太','平四','胡斐','张总管','王剑英','王剑杰','陈禹',
            '古若般','殷仲翔','福康安','赵半山','孙刚峰','吕小妹','钟四嫂','易吉','钟小二','钟阿四','胖商人','瘦商人',
            '凤南天', '凤七', '俞朝奉', '蛇皮张', '邝宝官', '凤一鸣', '大汉', '孙伏虎', '尉迟连', '杨宾', '中年武师',
            '程灵素','同桌后生','袁紫衣','刘鹤真','崔百胜','曹猛','蓝秦','王仲萍','张飞雄','慕容景岳','姜铁山','薛鹊',
            '王铁匠','姜小铁','田青文','张管家','聂钺','上官','褚轰','汪铁鹗','周铁鹤','曾铁鸥','秦耐之','姬晓峰','张九',
            '任通武','相国夫人','蔡威','汤沛','无青子','海兰弼','大智禅师','欧阳公政','西灵道人','文醉翁','周隆','郭玉堂',
            '齐伯涛','陈高波','安提督','宗雄','桑飞虹','倪不大','倪不小','常赫志','常伯志','上官铁生','哈赤大师','心砚','石双英',
            '刘之余','童怀道','李廷豹','石万嗔','木文察','陈家洛','无尘道长','德布','李沅芷','余鱼同','司徒雷','谢不当','黄希节'
        ]

        if sname in primname:
            return sname

        return None

    #检测雪山飞狐人名
    # 参数：待检测人名
    # 返回值：更正的人名
    def check_xueshanfeihu_name(self, sname: str) -> str:
        #《雪山飞狐》人物（共有25人）
        primname = [
            '于管家','田青文','左书僮','右书僮','平阿四','阮士忠','刘元鹤','杜希孟','周云阳','郑三娘','宝树','苗若兰','苗人凤',
            '范帮主','殷吉','胡一刀','胡夫人','胡斐','陶子安','陶百岁','曹云奇','琴儿','熊元献','静智大师','赛总管'
        ]

        if sname in primname:
            return sname

        return None

    #检测连诚诀人名
    # 参数：待检测人名
    # 返回值：更正的人名
    def check_lianchengjue_name(self, sname: str) -> str:
        #《连诚诀》人物（共有37人）
        primname = [
            '卜垣','丁典','万震山','马大鸣','万圭','水福','水岱','水笙','孙均','冯坦','平工头','刘乘风','血刀老祖','言达平',
            '汪啸风','张姓老者','陆天抒','吴坎','沈城','花铁干','狄云','宝象和尚','周圻','空心菜','鱼贩头子','桃红','耿天霜',
            '高管家','教书先生','铁匠','凌退思','凌霜华','菊友','梅念笙','戚芳','戚长发','鲁坤'
        ]

        if sname in primname:
            return sname

        return None

    #检测天龙八部人名
    # 参数：待检测人名
    # 返回值：更正的人名
    def check_tianlongbabu_name(self, sname : str) -> str:
        #《天龙八部》人物（共有169人）
        primname = [
            '刀白凤','丁春秋','马夫人','马五德','小翠','于光豪','巴天石','不平道人','邓百川','风波恶','甘宝宝','公冶乾','木婉清',
            '少林老僧','太皇太后','天狼子','天山童姥','王语嫣','乌老大','无崖子','云岛主','云中鹤','止清','白世镜','包不同','本参',
            '本观','本相','本因','出尘子','冯阿三','兰剑','古笃诚','过彦之','平婆婆','石清露','石嫂','司空玄','司马林','玄慈','玄寂',
            '玄苦','玄难','玄生','玄痛','叶二娘','竹剑','左子穆','华赫艮','乔峰','李春来','李傀儡','李秋水','刘竹庄','朴者和尚',
            '祁六三','全冠清','阮星竹','西夏宫女','许卓诚','朱丹臣','努儿海','阿碧','阿洪','阿胜','阿朱','阿紫','波罗星','陈孤雁',
            '鸠摩智','来福儿','孟师叔','宋长老','苏星河','苏辙','完颜阿古打','耶律洪基','耶律莫哥','耶律涅鲁古','耶律重元','吴长风',
            '吴光胜','吴领军','辛双清','严妈妈','余婆婆','岳老三','张全祥','单伯山','单季山','单叔山','单∩?单正','段延庆','段誉',
            '段正淳','段正明','范禹','范百龄','范骅','苟读','和里布','何望海','易大彪','郁光标','卓不凡','宗赞王子','哈大霸','姜师叔',
            '枯荣长老','梦姑','姚伯当','神山上人','神音','狮鼻子','室里','项长老','幽草','赵钱孙','赵洵','哲罗星','钟灵','钟万仇',
            '高升泰','龚光杰','贾老者','康广陵','秦红棉','虚竹','容子矩','桑土公','唐光雄','奚长老','徐长老','诸保昆','崔百泉',
            '崔绿华','符敏仪','黄眉和尚','菊剑','聋哑婆婆','梅剑','萧远山','游骥','游驹','游坦之','程青霜','傅思归','葛光佩','缘根',
            '智光大师','鲍千灵','褚万里','瑞婆婆','端木元','黎夫人','薛慕华','慕容博','慕容复','谭公','谭婆','谭青','摘星子','慧方',
            '慧观','慧净','慧真','穆贵妃','赫连铁树'
        ]

        if sname in primname:
            return sname

        return None

    #检测射雕英雄传人名
    # 参数：待检测人名
    # 返回值：更正的人名
    def check_shediaoyingxiongzhuan_name(self, sname: str) -> str:
        #《射雕英雄传》人物（共有97人）
        primname = [
            '一灯大师','马青雄','马钰','小沙弥','木华黎','丘处机','沈青刚','书记','书生','天竺僧人','王处一','王罕','尹志平','包惜弱',
            '冯衡','术赤','农夫','孙不二','札木合','华筝','李萍','刘玄处','刘瑛姑','吕文德','乔寨主','曲三','曲傻姑','全金发','汤祖德',
            '朱聪','陈玄风','赤老温','瘦丐','陆乘风','陆冠英','沙通天','吴青烈','杨康','杨铁心','余兆兴','张阿生','张十五','忽都虎',
            '欧阳峰','欧阳克','梅超风','铁木真','拖雷','者勒米','段天德','枯木','周伯通','郭靖','郭啸天','郝大通','洪七公','侯通海',
            '姜文','柯镇恶','南希仁','胖妇人','胖丐','胖子','哑梢公','都史','钱青健','桑昆','盖运聪','黄蓉','黄药师','梁长老','梁子翁',
            '渔人','博尔忽','博尔术','程瑶迦','韩宝驹','韩小莹','焦木和尚','鲁有脚','穆念慈','彭长老','彭连虎','童子','窝阔台','简长老',
            '简管家','裘千仞','裘千丈','察合台','酸儒文人','谭处端','黎生','樵子','灵智上人','完颜洪烈','完颜洪熙'
        ]

        if sname in primname:
            return sname

        return None

    #检测白马啸西风人名
    # 参数：待检测人名
    # 返回值：更正的人名
    def check_baimaxiaoxifeng_name(self, sname: str) -> str:
        #《白马啸西风》人物(共有17人)
        primname = [
            '李三','霍元龙','史仲俊','陈达海','上官虹','李文秀','马家骏','苏普','苏鲁克','车尔库','阿曼','桑斯','瓦尔拉齐','云强盗',
            '全强盗','宁强盗','丁同'
            ]

        if sname in primname:
            return sname

        return None

    #检测鹿鼎记人名
    # 参数：待检测人名
    # 返回值：更正的人名
    def check_ludingji_name(self, sname: str) -> str:
        #《鹿鼎记》人物(共有183人)
        #'小桂子','小玄子(玄烨)
        primname = [
            '九难','卫周祚','马喇','马佑','马宝','马博仁','于八','马超兴','马齐','心溪','韦小宝','韦春花','毛东珠',
            '巴颜法师','巴泰','方怡','风际中','邓炳春','云素梅','无根道人','王潭','方大洪','五符','元义方','巴郎星',
            '王武通', '王进宝', '王琪', '双儿', '史松', '冯难敌', '邝天雄', '平威', '白寒松', '白寒枫', '卢一峰', 
            '归辛树', '玄真道人', '司徒鹤', '司徒伯雷','对喀纳','冯锡范','孙思克','归钟','归二娘','玉林','汤若望',
            '李自成','老吴','守备','米思翰','江百胜','齐元凯','华伯斯基','齐洛诺夫','西奥图三世','刘一舟','沐剑声',
            '庄夫人','许雪亭','多隆','行痴','祁清彪','关安基','吕留良','阿珂','李西华','吕葆中','吕毅中','行颠',
            '庄廷龙', '庄允城', '陆高轩', '杜立德', '吴之荣', '苏菲亚', '陈圆圆','罕贴摩','吴大鹏','沐剑屏','吴三桂',
            '阿济赤','阿尔尼','张淡月','苏荃','苏冈','吴六奇','李式开','李力世','陈近南','吴应熊','杨溢之','佟国纲',
            '吴立身', '张康年', '张勇', '张妈', '吴宝宇', '何惕守', '劳太监', '明珠', '皇甫阁', '柳燕', '图海道', '杰书', 
            '郎师傅', '图尔布青', '净清', '净济', '林兴珠', '林永超', '柳大洪', '呼巴音', '昌齐', '郑克塽', '赵齐贤', 
            '建宁公主','茅十八','神照上人','洪朝','姚春','施琅','费要多罗','胡逸之','南怀仁','钟志灵','洪安通','胡德第',
            '姚必达', '赵良栋', '查继左', '胖头陀', '郝太监', '徐天川', '陶红英', '索额图', '教士', '陶师傅', '高里津', 
            '敖彪', '高颜超', '钱老本', '海大富', '殷锦', '贾老六', '笔贴式','顾炎武','夏国相','桑结','晦聪禅师','章老三',
            '黄甫','黄金魁','崔瞎子','黄宗羲','菊芳','彭参将','葛尔丹','程维藩','温有方','温有道','舒化龙','曾柔','富春',
            '葛通', '路副将', '雷一啸', '瘦头陀', '蕊初','瑞栋','蔡德忠','察尔珠','潘先生','澄光','澄通','澄观','澄心',
            '澄识','樊纲','慕天颜','鳌拜','玄烨'
            ]

        #鹿鼎记
        if sname == '小玄子' or sname == '皇上' or sname=='康熙':
            sname = '玄烨'
        elif sname == '小桂子':
            sname = '韦小宝'

        if sname in primname:
            return sname

        return None

    #检测笑傲江湖人名
    # 参数：待检测人名
    # 返回值：更正的人名
    def check_xiaoaojianghu_name(self, sname: str) -> str:
        #《笑傲江湖》人物（共有160人）
        primname = [
            '卜沉','丁坚','丁勉','上官云','万大平','于人豪','于嫂','不戒和尚','长青子','仇松年','丹青生','邓八公','方人智','方生',
            '方证','风清扬','计无施','天门道人','天松道人','天乙道人','王伯奋','王诚','王二叔','王夫人','王家驹','王家骏','王元霸',
            '王仲强','白二','白熊','丛不弃','莫大','农妇','东方不败','乐厚','令狐冲','宁中则','平夫人','平一指','申人俊','史镖头',
            '史登达','司马大','田伯光','仪和','仪琳','仪清','玉玑子','玉灵道人','玉磬子','玉音子','玉钟子','左冷禅','成不忧','成高道人',
            '冲虚道长','吉人通','老不死','老头子','刘菁','刘芹','刘正风','米为义','齐堂主','曲非烟','曲洋','任我行','英颚','西宝','向大年',
            '向问天','陈七','陈歪嘴','迟百诚','狄镖头','狄修','定静师太','杜长老','何三七','季镖头','劳德诺','陆伯','陆大有','任盈盈',
            '沙天江','秃笔翁','吴柏英','吴天德','辛国梁','严三星','杨莲亭','余沧海','余人彦','岳灵珊','张夫人','张金鏊','定逸','建除',
            '林平之','林远图','林震南','罗人杰','易国梓','易师爷','易堂主','英白罗','英长老','岳不群','郑镖头','郑萼','周孤桐','封不平',
            '洪人雄','侯人英','觉月','施戴子','施令威','闻先生','哑婆婆','钟镇','祝镖头','祖千秋','高克新','高明根','贾布','麻衣汉子',
            '费彬','秦娟','秦伟帮','舒奇','桑三娘','桃干仙','桃根仙','桃花仙','桃实仙','桃叶仙','桃枝仙','陶钧','夏老拳师','崔镖头',
            '黄伯流','黄国柏','黄钟公','假东方不败','绿竹翁','清虚道人','游迅','葛长老','黑白子','黑熊','鲁连荣','童百熊','鲍大楚',
            '解风','蓝凤凰','谭迪人','震山子','木高峰','贾人达','梁发'
        ]

        if sname in primname:
            return sname

        return None

    #检测书剑恩仇录人名
    # 参数：待检测人名
    # 返回值：更正的人名
    def check_shujianenchoulu_name(self, sname: str) -> str:
        #《书剑恩仇录》人物（共有120人）
        primname = [
            '大痴','卫春华','马善均','于万亭','大癫','马敬侠','大苦','马真','孙大善','万庆澜','马大挺','上官毅山','文泰来','心砚',
            '天镜','木卓伦','元伤','元痛','元悲','方有德','王维扬','王道','贝人龙','尹章垓','天虹禅师','冯辉','石双英','玉如意',
            '平旺先','龙骏','白振','孙老三','孙克通','安健刚','成璜','兆惠','关明梅','李可秀','朱祖荫','李沅芷','吴国栋','迟玄',
            '沈德潜','杨成协','余鱼同','陈家洛','张安官','纳斯尔丁•阿凡提','玛米尔','陆菲青','孟健雄','陈正德','宋善朋','张召重',
            '言伯乾','汪浩天','阿凡提妻','阿里','宋天保','武铭','凯别兴','郑板桥','忽伦大虎','周绮','忽伦二虎','忽伦三虎','忽伦四虎',
            '周阿三','范中恩','和尔大','罗信','周仲英','呼音克','周大奶奶','周英杰','赵半山','哈合台','皇太后','骆冰','胡老爷',
            '唐六爷','阎世章','阎世魁','徐天宏','袁枚','顾金标','桑拉巴','袁士霄','教长','钱正伦','梅良鸣','曹司朋','章进','曹能',
            '常伯志','常赫志','乾隆皇帝','韩春霖','蒋天寿','瑞芳','晴画','焦文期','蒋四根','蒋士铨','褚圆','曾图南','喀丝丽','童兆和',
            '韩文冲','覃天丞','彭三春','德鄂','腾一雷','瑞大林','福康安','霍青桐','霍阿伊','戴永明','无尘道人'
        ]

        if sname in primname:
            return sname

        return None

    #检测神雕侠侣人名
    # 参数：待检测人名
    # 返回值：更正的人名
    def check_shendiaoxialv_name(self, sname : str) -> str:
        #《神雕侠侣》人物（共有126人）
        primname = [
            '子聪','丁大全','人厨子','九死生','马钰','小棒头','大头鬼','马光佐','小王将军','小龙女','尹志平','丘处机','王处一',
            '王十三','公孙止','少妇','王志坦','王惟忠','无常鬼','尹克西','天竺僧','公孙绿萼','孙婆婆','孙不二','皮清云','申志凡',
            '冯默风','讨债鬼','史伯威','史仲猛','史叔刚','史季强','史孟龙','圣因师太','尼摩星','李莫愁','达尔巴','刘处玄','朱子柳',
            '曲傻姑','吕文德','祁志诚','李志常','刘瑛姑','吊死鬼','百草仙','陆鼎立','陆二娘','阿根','张志光','完颜萍','陆冠英',
            '宋德方','陈大方','宋五','沙通天','灵智上人','郭靖','郭芙','郭襄','霍都','张君宝','张一氓','陈老丐','张二叔','陆无双',
            '杨过','武三通','武敦儒','武修文','武三娘','林朝英','耶律晋','耶律楚材','耶律燕','忽必烈','丧门鬼','俏鬼','蒙哥','狗头陀',
            '青灵子','欧阳峰','耶律齐','金轮法王','周伯通','洪凌波','点苍渔隐','柔儿','郭破虏','侯通海','觉远大师','柯镇恶','赵志敬',
            '洪七公','姬清玄','笑脸鬼','鹿清笃','崔志方','鄂尔多','萨多','黄药师','黄蓉','程遥迦','鲁有脚','彭连虎','韩无垢','童大海',
            '韩老丐','彭长老','蓝天和一灯大师瘦丐','程瑛','雷猛','裘千尺','煞神鬼','催命鬼','裘千仞','赫大通','潇湘子','樊一翁',
            '藏边大丑','藏边二丑','藏边三丑','藏边四丑','藏边五丑'
        ]

        if sname in primname:
            return sname

        return None

    #检测侠客行人名
    # 参数：待检测人名
    # 返回值：更正的人名
    def check_xiakexing_name(self, sname: str) -> str:
        #《侠客行》人物（共有67人）
        primname = [
            '丁不三','丁不四','丁珰','大悲老人','贝海石','木岛主','王掌柜','元澄道人','王万仞','王老六','尤得胜','天虚','风良',
            '展飞','杨光','闵柔','汉子龙岛主','冯振武','孙万年','司徒横','石清','白万剑','石中玉','白阿绣','史小翠','石破天',
            '李四','李大元','安奉日','米横野','李万山','老李','冲虚','吕正平','齐自勉','成自学','西门观止','张三','吴道通','花万紫',
            '白自在','邱山风','陈冲之','汪万翼','周牧','侍剑','呼延万善','范一飞','郑光芝','封万里','柯万钧','闻万夫','胡大哥','耿万钟',
            '高三娘子','梁自进','梅文馨','梅芳姑','黄面道人','温仁厚','谢烟客','褚万春','照虚','解文豹','廖自砺','丑脸汉子'
        ]

        if sname in primname:
            return sname

        return None

    #检测倚天屠龙记人名
    # 参数：待检测人名
    # 返回值：更正的人名
    def check_yitiantulongji_name(self, sname: str) -> str:
        #《倚天屠龙记》人物（共有184人）
        primname = [
            '卜泰','丁敏君','马法通','卫天望','卫四娘','小翠','小虹','小玲','小凤','小昭','卫璧','王难姑','元广波','邓愈','方天劳',
            '云鹤','韦一笑','王八衰天鸣方丈','无相禅师','无色','方东白','五姑','贝锦仪','乌旺阿普','王保保','太虚子','史镖头','灭绝师太',
            '史火龙','史红石','叶长青','孙三毁','白龟寿','司徒千钟','执法长老','传功长老','汤和','朱元璋','祁天彪','纪晓芙','朱长龄',
            '西华子','刘敖','阳顶天','齐心宝树王','庄铮','李四摧','过三拳','李天恒','刚相','朱九真','乔福','苏梦清','陈友谅','季长老',
            '花云','吴良','吴祯','张无忌','麦鲸','何足道','冷谦','杜百当','杨逍','辛然','妙风使','邵鹤','邵燕','吴劲草','寿南山','吴六破',
            '张中','何太冲','孟正鸿','灵虚','宋青书','张三丰','阿二','阿三','杨不悔','麦少帮主','杨姐姐','宋远桥','张松溪','张翠山',
            '苏习之','周芷若','郑长老','宗维侠','范遥','拨速台','空闻','空智','空性','空见','空性','周五输','郑七灭','金花婆婆','武青婴',
            '周颠','明月','武烈','易三娘','说不得','胡青牛','泉建男','郝密','闻苍松','哈总管','觉远','赵敏','赵一伤','封坛主','贺老三',
            '欧阳牧之','郭襄','宫九佳','姚清泉','胡青羊','俞莲舟','俞岱岩','都大锦','徐达','唐洋','高老者','圆真(成昆)','唐文亮','高则成',
            '流云使','夏胄','秦老五','圆音','圆业','圆心','钱二败','殷野王','殷天正','殷无禄','殷无福','殷无寿','殷离','班淑娴','殷素素',
            '殷梨亭','莫声谷','常敬之','常遇春','清风常胜宝树王','平等宝树王','俱明宝树王','渡劫','渡难','渡厄','常金鹏','鹿杖客','掌钵龙头',
            '掌棒龙头','彭莹玉','谢逊','蒋涛','辉月使','詹春','程坛主','韩千叶','韩林儿','矮老者','简捷','静虚师太','静玄师太','静空','静照',
            '静迦','静慧','察罕特穆尔','鲜于通','摩诃巴思','德成','颜恒','潘天耕','鹤笔翁','薛公远'
        ]

        if sname in primname:
            return sname

        return None

    #检测碧血剑人名
    # 参数：待检测人名
    # 返回值：更正的人名
    def check_bixuejian_name(self, sname: str) -> str:
        #《碧血剑》人物（共有108人）
        primname = [
            '丁游','小菊','万里风','水鉴','义生','马公子','玉真子','水云道人','王师兄','木桑道长','归辛树','归二娘','孙仲寿','田见秀',
            '龙德邻','孙仲尹','冯同知','宁完我','石骏','史秉文','史秉光','冯难敌','冯不摧','冯不破','白脸人','安大娘','刘芳亮','吕七',
            '杨景亭','刘培生','安剑清','多尔衮','刘宗敏','红娘子','朱安国','老王','安小慧','齐云','张朝唐','张信','张康','杨鹏举','张春九',
            '沙老大','闵子华','吴平','沙广天','孟伯飞','孟铸','张若谷','孟铮','李岩','单铁生','陈圆圆','宋献策','应松','岑其斯','何红药',
            '李自成','阿九','何铁手','郑起云','范文程','罗大千','罗立如','彼得','若克琳','荣彩','洞玄','侯飞文','皇太极','祖大寿','倪浩',
            '哑巴','胡桂南','胡老三','洪胜海','秦栋','钱通四','高师弟','袁承志','夏雪宜','崔秋山','黄真','崔希敏','黄二毛子','曹化淳',
            '黄须人','梅剑和','温正','温南扬','焦公礼','程青竹','褚红柏','董开山','温方施','温方山','温方悟','温青','温方达','温方义',
            '焦宛儿','温仪','鲍承先','谭文理','黎刚','潘秀达','穆人清'
        ]

        if sname in primname:
            return sname

        return None

    #检测鸳鸯刀人名
    # 参数：待检测人名
    # 返回值：更正的人名
    def check_yuanyangdao_name(self, sname: str) -> str:
        #《鸳鸯刀》人物（共有15人）
        primname = [
            '任飞燕','刘於义','杨夫人','花剑影','林玉龙','周威信','卓天雄','逍遥子','袁夫人','袁冠南','常长风','盖一鸣','萧半和',
            '萧中慧','杨中慧','书僮'
        ]

        if sname in primname:
            return sname

        return None


class task_bookgraph(taskinterface):
    
    def __init__(self) -> None:
        self._name = const.BOOKGRAPH_NAME
        self._tasktype = 'tools'
        self._parameter = ''
        
        self._pathfile = ''
        self._filename = ''

        super().__init__()

    #分词，生成excel文件内容
    def _fCutWord(self, txtFilename: str) ->None:
        
        self._pathfile = txtFilename
        s = os.path.basename(txtFilename)
        self._filename = s.split('.',1)[0]

        # 分词
        dfname = pd.DataFrame()
        dfname['name'] = None
        dfname['symbolSize'] = None
        dflink = pd.DataFrame()
        dflink['source'] = None
        dflink['target'] = None
        dflink['value'] = None

        ckn = checkname()
        ckn._fupdatefunc(self._filename)

        lineNames = []  # 缓存变量，保存对每一段分词得到当前段中出现的人物名称

        fsize = os.path.getsize(txtFilename)
        if fsize <= 0:
            return
        pbar = tqdm(total=fsize, desc=const.BOOKGRAPH_NAME)

        with codecs.open(txtFilename, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f.readlines():

                pbar.update(len(str(line).encode())) #换算为字节数

                poss = pseg.cut(line)  # 分词，返回词性
                lineNames =[]  # 为本段增加一个人物列表

                for w in poss:
                    if w.flag != 'nr' or len(w.word) < 2:# or w.word in excludes:
                        continue  # 当分词长度小于2或该词词性不为nr（人名）时认为该词不为人名

                    #检测
                    strname = ckn.checkfunc(w.word)
                    if strname == None:
                        continue

                    #处理人物列表
                    if strname in dfname['name'].values:
                        row = dfname.loc[dfname['name'] == strname].index[0]
                        dfname.loc[row, 'symbolSize'] = dfname.loc[row,
                                                                'symbolSize'] + 1
                    else:
                        dfname = dfname.append(
                            {"name": strname, "symbolSize": 1}, ignore_index=True)

                    #处理人物关系
                    lineNames.append(strname)  # 为当前段的环境增加一个人物

                #处理人物关系，加入到dataframe中
                lineNames = list(set(lineNames))  #去重

                for sname in lineNames:
                    lineNames.remove(sname)

                    dftmp = dflink.loc[dflink['source'] == sname ]
                    dftmp = dftmp.append(dflink.loc[dflink['target'] == sname])

                    for sname1 in lineNames:
                        row = None
                        if not dftmp.empty:
                            dftmp1 = dftmp.loc[dftmp['target'] == sname1]
                            dftmp1 = dftmp1.append(
                                dftmp.loc[dftmp['source'] == sname1])
                            if not dftmp1.empty:
                                row = dftmp1.index[0]
                        if row == None:
                            #未找到关联，新建立
                            dflink = dflink.append(
                                {"source": sname, "target": sname1, "value": 1}, ignore_index=True)
                        else:
                            #已有关联，读取原value值+1
                            dflink.loc[row, 'value'] = dflink.loc[row, 'value'] + 1

            f.close()

        pbar.close()

        #循环结束，写文件
        with pd.ExcelWriter(const.EXCEL_FILE) as writer:
            dfname.to_excel(writer, const.SHEET_NAME,index=False)
            dflink.to_excel(writer, const.SHEET_LINK, index=False)

            writer.save()
        #writer.close()

    def _fDrawGraph(self) -> None:
        # 从excel中读取数据，并化出节点图

        dfname = pd.read_excel(const.EXCEL_FILE,const.SHEET_NAME)
        dflink = pd.read_excel(const.EXCEL_FILE, const.SHEET_LINK)

        '''
        print(dfname)
        print(dflink)

        row_name = dfname.shape[0]
        column_name = dfname.shape[1]
        row_link = dflink.shape[0]
        column_link = dflink.shape[1]
        '''

        list_name = dfname.values.tolist()
        nodes = []
        maxnum = -1
        for i in range(0,len(list_name)):
            nodes.append({"name":list_name[i][0], "symbolSize":list_name[i][1]})
            if list_name[i][1] > maxnum:
                maxnum = list_name[i][1]
        #print(nodes)

        #缩放节点，差距太大显示不对
        pos = maxnum / 10
        for i in range(0,len(nodes)):
            num1 = nodes[i]['symbolSize']
            num1 = (num1 / pos ) * 10
            if(num1 < 10):
                num1 = 10
            nodes[i]['symbolSize'] = num1

        list_link = dflink.values.tolist()
        links = []
        for j in range(0, len(list_link)):
            links.append(
                {"source":list_link[j][0], "target":list_link[j][1],"value":list_link[j][2]})
        #print(links)

        c = (
            Graph()
            .add("", nodes, links, repulsion=8000)
            .set_global_opts(title_opts=opts.TitleOpts(title=self._filename))
            .render("graph_base.html")
        )

    
    def _fupdateparameter(self) -> str:
        d = dict()
        
        d.setdefault('bookfile', self._pathfile)
        
        s : str
        s = json.dumps(d)
        
        self._parameter = s
        return s

    def _fconvertparmaeter(self, parameter: str) -> None:
        '''
        bookfile
        '''
        d : dict
        ret = 0
        try:
            d = json.loads(parameter)

            self._pathfile = d['bookfile']
        except:
            ret = -1
        return ret
    
    def _fcheckparmaeter(self) -> bool:
        if len(self._pathfile) <= 0:
            return False
        return True

    def run(self) -> int:
        if self._fcheckparmaeter():
            self._fCutWord(self._pathfile)
            self._fDrawGraph()
        
        return 0

    def opensetup(self) -> int:
        fname, ftype = QFileDialog.getOpenFileName(None, '选择打开的TXT文件',os.getcwd(),'TXT files(*.txt)')
        if len(fname) > 0:
            self._pathfile = fname
            
            self._fupdateparameter()
            
            return 0
        
        return -1

    def getname(self) -> str:
        return self._name

    def gettype(self) -> str:
        return self._tasktype

    def getparameter(self) -> str:
        return self._parameter

    def setparameter(self, parameter: str) -> int:
        self._parameter = parameter
        if len(parameter) > 0:
            return self._fconvertparmaeter(parameter)
        return 0

    def getpercent(self) -> int:
        return self._percent

