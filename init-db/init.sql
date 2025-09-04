-- 这个脚本将在数据库首次创建时自动执行
-- 我们首先连接到正确的数据库
-- \c novel_characters_db;

-- =======================================================
-- ==             插入世界观设定 (Lore) 数据            ==
-- =======================================================

-- 种族 (Race) 设定
INSERT INTO lore_entries (category, key, name, description, attributes) VALUES
(
    'Race',
    'Human',
    '人类',
    '最具适应力和数量最多的种族，遍布大陆的各个角落。他们寿命短暂，但充满野心和创造力，能够在各种环境中建立文明。',
    '{"traits": ["适应性强", "多才多艺", "社会性强"], "typical_classes": ["战士", "法师", "盗贼"]}'::jsonb
),
(
    'Race',
    'Elf',
    '精灵',
    '优雅而长寿的古老种族，与自然和魔法有着深刻的联系。他们通常居住在古老的森林或与世隔绝的城市中，是天生的弓箭手和法师。',
    '{"traits": ["长寿", "感知敏锐", "天生亲和魔法", "夜视能力"], "typical_classes": ["游侠", "德鲁伊", "大法师"]}'::jsonb
),
(
    'Race',
    'Dwarf',
    '矮人',
    '强壮而坚韧的山地民族，以其精湛的锻造工艺、对矿石和宝石的热爱以及豪迈的性格而闻名。他们是忠诚的盟友和顽强的战士。',
    '{"traits": ["坚韧", "工艺大师", "黑暗视觉", "抗毒性"], "typical_classes": ["战士", "圣骑士", "符文师"]}'::jsonb
),
(
    'Race',
    'Orc',
    '兽人',
    '一个崇尚力量和荣誉的部落种族，通常体格魁梧，意志坚定。尽管外界对他们有刻板印象，但兽人社会内部有着复杂的传统和萨满信仰。',
    '{"traits": ["力量强大", "意志坚定", "部落荣誉"], "typical_classes": ["狂战士", "萨满", "酋长"]}'::jsonb
);

-- 阵营 (Alignment) 设定
INSERT INTO lore_entries (category, key, name, description) VALUES
(
    'Alignment',
    'Lawful Good',
    '守序善良',
    '信奉通过秩序、规则和高尚的品德来创造至善的世界。他们是人民的守护者，是正义的化身，如圣骑士和正直的君王。'
),
(
    'Alignment',
    'Neutral Good',
    '中立善良',
    '致力于行善，但不拘泥于秩序或混乱的教条。他们相信良知是最好的指引，会尽其所能帮助他人，如善良的牧师或仁慈的隐士。'
),
(
    'Alignment',
    'Chaotic Good',
    '混乱善良',
    '追随自己内心的善良，并蔑视一切可能阻碍他们行善的官僚和规则。他们是自由的斗士和反抗暴政的英雄，如侠盗罗宾汉。'
);

-- 插入角色 1: 赛博朋克侦探
INSERT INTO characters (id, name, nickname, age, occupation, height_cm, image_filename, gender, build, race, alignment, status, bloodline, measurements, personality_details, appearance_details, background_details, speech_patterns) VALUES
(
    'a1b2c3d4-e5f6-7890-1234-567890abcdef', -- 使用一个固定的 UUID 以便测试
    '凯文',
    '幽灵',
    32,
    '信息掮客 / 私家侦探',
    185,
    'kaelen_vance.jpg',
    'MALE',
    'ATHLETIC',
    'HUMAN',
    'CHAOTIC_NEUTRAL',
    'ALIVE',
    'NOBLE',
    '{}'::jsonb, -- 空的 measurements JSONB
    '{
        "core_traits": ["愤世嫉俗", "观察力敏锐", "足智谋", "忠于自己的准则", "有黑色幽默感"],
        "mbti": "ISTP",
        "strengths": "在压力下保持冷静，能从海量数据中找到线索。",
        "weaknesses": "不信任他人，有轻微的神经增强剂依赖。",
        "likes": "雨夜、爵士乐、老式黑白电影",
        "dislikes": "巨型企业、官僚主义、虚伪的政客"
    }'::jsonb,
    '{
        "hair": "黑色短发，右侧有几缕被染成银色",
        "eyes": "深棕色，右眼被一个发出幽蓝光芒的义眼取代",
        "distinguishing_features": "脖子后面有一个二维码纹身，左臂是机械义肢。"
    }'::jsonb,
    '{
        "hometown": "霓虹城第7区",
        "key_life_events": "曾是巨型企业''奥姆尼科''的网络安全专家，因发现公司内部的黑暗秘密而被陷害，被迫在地下世界谋生。"
    }'::jsonb,
    '{
        "voice": "低沉、略带沙哑",
        "common_phrases": ["每个比特都会说谎，除非你强迫它说真话。", "信息就是货币，朋友。"]
    }'::jsonb
);

-- 插入角色 2: 精灵法师/学者
INSERT INTO characters (id, name, nickname, age, occupation, height_cm, image_filename, gender, build, race, alignment, status, bloodline, measurements, personality_details, appearance_details, background_details, speech_patterns) VALUES
(
    'b2c3d4e5-f6a7-8901-2345-67890abcdef1',
    '兰斯特',
    '星语者',
    120,
    '星辰高塔的大法师 / 古代史学者',
    175,
    'lyra_silvanus.jpg',
    'FEMALE',
    'SLIM',
    'ELF',
    'LAWFUL_GOOD',
    'ALIVE',
    'NOBLE',
    '{
        "bust_cm": 86,
        "waist_cm": 60,
        "hip_cm": 89
    }'::jsonb,
    '{
        "core_traits": ["智慧", "耐心", "仁慈", "求知欲强", "一丝不苟"],
        "mbti": "INFJ"
    }'::jsonb,
    '{
        "hair": "月白色的长发，常常编织着星辰样式的银饰",
        "eyes": "像紫水晶一样清澈的紫色眼眸",
        "clothing_style": "优雅的白色或蓝色长袍，上面绣有复杂的魔法符文。"
    }'::jsonb,
    '{
        "hometown": "银月森林"
    }'::jsonb,
    '{}'::jsonb
);

-- 插入角色 3: 兽人部落的年轻酋长
INSERT INTO characters (id, name, age, occupation, height_cm, image_filename, gender, build, race, alignment, status, bloodline, measurements, personality_details, appearance_details, background_details, speech_patterns) VALUES
(
    '3fa85f64-5717-4562-b3fc-2c963f66afa6',
    '格罗姆',
    25,
    '血牙部落酋长',
    210,
    'grommash.jpg',
    'MALE',
    'MUSCULAR',
    'ORC',
    'NEUTRAL_GOOD',
    'ALIVE',
    'ANCIENT',
    '{}'::jsonb,
    '{
        "core_traits": ["勇敢", "直率", "有责任感", "尊重传统", "略显冲动"],
        "strengths": "天生的领袖，拥有强大的力量和战斗技巧。",
        "weaknesses": "对复杂的计谋和背叛缺乏防备心。",
        "likes": "狩猎、篝火晚会、荣誉决斗",
        "dislikes": "懦弱、欺骗、不必要的杀戮"
    }'::jsonb,
    '{
        "skin_tone": "绿色皮肤",
        "distinguishing_features": "脸上有一道从额头划过左眼的旧伤疤，下颚有两颗突出的獠牙。"
    }'::jsonb,
    '{
        "key_life_events": "在父亲去世后，通过一场荣誉决斗赢得了酋长之位，致力于带领部落在艰难的环境中生存下去。"
    }'::jsonb,
    '{
        "voice": "洪亮、粗犷"
    }'::jsonb
);

INSERT INTO characters (id, name, nickname, age, occupation, height_cm, image_filename, gender, build, race, alignment, status, bloodline, measurements, personality_details, appearance_details, background_details, speech_patterns) VALUES
(
    'c3d4e5f6-a7b8-9012-3456-7890abcdef12',
    '格伦·石须',
    '铁砧',
    250,
    '铁炉堡的传奇铁匠 / 符文守护者',
    145,
    'grom_stonebeard.jpg',
    'MALE',
    'HEAVYSET',
    'DWARF',
    'LAWFUL_NEUTRAL',
    'ALIVE',
    'ANCIENT',
    '{}'::jsonb,
    '{
        "core_traits": ["固执", "忠诚", "勇敢", "技艺精湛", "沉默寡言"],
        "mbti": "ISTJ"
    }'::jsonb,
    '{
        "hair": "火红色的长胡子，精心编成数条辫子，上面镶嵌着符文石",
        "eyes": "深邃的棕色眼眸，如同熔岩",
        "clothing_style": "厚重的符文铠甲，手持一柄巨大的战锤"
    }'::jsonb,
    '{
        "hometown": "铁炉堡"
    }'::jsonb,
    '{}'::jsonb
);

-- 角色3: 勇猛的兽人酋长
INSERT INTO characters (id, name, nickname, age, occupation, height_cm, image_filename, gender, build, race, alignment, status, bloodline, measurements, personality_details, appearance_details, background_details, speech_patterns) VALUES
(
    'd4e5f6a7-b8c9-0123-4567-890abcdef123',
    '杜尔克·碎颅者',
    '鲜血之爪',
    45,
    '血牙部落酋长',
    210,
    'durok_skullcrusher.jpg',
    'MALE',
    'MUSCULAR',
    'ORC',
    'CHAOTIC_NEUTRAL',
    'ALIVE',
    'COMMON',
    '{}'::jsonb,
    '{
        "core_traits": ["好战", "狡猾", "有领导力", "实用主义", "不畏强权"],
        "mbti": "ESTP"
    }'::jsonb,
    '{
        "hair": "黑色的长发，梳成一束顶髻",
        "eyes": "凶狠的红色眼睛",
        "clothing_style": "由皮革和兽骨制成的简易护甲，身上有许多战斗疤痕和部落图腾纹身"
    }'::jsonb,
    '{
        "hometown": "破碎平原"
    }'::jsonb,
    '{}'::jsonb
);

-- 角色4: 高尚的人类骑士
INSERT INTO characters (id, name, nickname, age, occupation, height_cm, image_filename, gender, build, race, alignment, status, bloodline, measurements, personality_details, appearance_details, background_details, speech_patterns) VALUES
(
    'e5f6a7b8-c9d0-1234-5678-90abcdef1234',
    '亚瑟·潘德拉贡',
    '晨曦之刃',
    32,
    '圣光骑士团团长',
    185,
    'arthur_pendragon.jpg',
    'MALE',
    'ATHLETIC',
    'HUMAN',
    'LAWFUL_GOOD',
    'ALIVE',
    'ROYAL',
    '{}'::jsonb,
    '{
        "core_traits": ["正直", "富有同情心", "天生的领袖", "有责任感", "理想主义"],
        "mbti": "ENFJ"
    }'::jsonb,
    '{
        "hair": "灿烂的金色短发",
        "eyes": "坚定而温暖的蓝色眼眸",
        "clothing_style": "闪亮的全身板甲，披着印有王国徽章的白色披风"
    }'::jsonb,
    '{
        "hometown": "卡美洛王城"
    }'::jsonb,
    '{}'::jsonb
);

-- 角色5: 混乱的哥布林盗贼
INSERT INTO characters (id, name, nickname, age, occupation, height_cm, image_filename, gender, build, race, alignment, status, bloodline, measurements, personality_details, appearance_details, background_details, speech_patterns) VALUES
(
    'f6a7b8c9-d0e1-2345-6789-0abcdef12345',
    '斯尼克',
    '影贼',
    25,
    '盗贼 / 炼金术士',
    95,
    'snik_goblin.jpg',
    'MALE',
    'SLIM',
    'GOBLIN',
    'CHAOTIC_EVIL',
    'ALIVE',
    'UNKNOWN',
    '{}'::jsonb,
    '{
        "core_traits": ["贪婪", "神经质", "对爆炸物有异常的热情", "机会主义", "胆小但狡诈"],
        "mbti": "ENTP"
    }'::jsonb,
    '{
        "hair": "稀疏的绿色头发",
        "eyes": "滴溜溜转的黄色大眼睛",
        "clothing_style": "破旧的皮甲，腰带上挂满了各种小瓶子、工具和偷来的小玩意"
    }'::jsonb,
    '{
        "hometown": "污水巷"
    }'::jsonb,
    '{}'::jsonb
);

-- 角色6: 冷酷的仿生人刺客
INSERT INTO characters (id, name, nickname, age, occupation, height_cm, image_filename, gender, build, race, alignment, status, bloodline, measurements, personality_details, appearance_details, background_details, speech_patterns) VALUES
(
    'a7b8c9d0-e1f2-3456-7890-1bcdef123456',
    '单元734',
    '幽灵',
    5,
    '秘密组织的刺客',
    180,
    'unit_734.jpg',
    'NON_BINARY',
    'ATHLETIC',
    'ANDROID',
    'TRUE_NEUTRAL',
    'ALIVE',
    'UNKNOWN',
    '{}'::jsonb,
    '{
        "core_traits": ["逻辑至上", "高效", "沉默", "任务导向", "缺乏情感表达"],
        "mbti": "ISTP"
    }'::jsonb,
    '{
        "hair": "银白色合成纤维短发",
        "eyes": "发出淡蓝色光芒的电子眼",
        "clothing_style": "贴身的黑色纳米作战服，能适应各种环境"
    }'::jsonb,
    '{
        "hometown": "“摇篮”实验室"
    }'::jsonb,
    '{}'::jsonb
);

-- 角色7: 化为人形的古龙
INSERT INTO characters (id, name, nickname, age, occupation, height_cm, image_filename, gender, build, race, alignment, status, bloodline, measurements, personality_details, appearance_details, background_details, speech_patterns) VALUES
(
    '89012345-6789-0abc-def1-234567890abc',
    '伊格尼丝',
    '烬心',
    8000,
    '沉睡的古龙 / 历史的观察者',
    178,
    'ignis_dragon.jpg',
    'FEMALE',
    'SLIM',
    'DRAGON',
    'NEUTRAL_GOOD',
    'ALIVE',
    'DIVINE',
    '{
        "bust_cm": 92,
        "waist_cm": 64,
        "hip_cm": 94
    }'::jsonb,
    '{
        "core_traits": ["古老而智慧", "慵懒", "对凡人事物感到有趣", "拥有强大的力量但很少使用", "守护着某种秘密"],
        "mbti": "INTP"
    }'::jsonb,
    '{
        "hair": "如同燃烧火焰般的深红色长卷发",
        "eyes": "金色竖瞳，偶尔会闪烁着火焰",
        "clothing_style": "华丽的深色长裙，配有黑曜石和黄金饰品"
    }'::jsonb,
    '{
        "hometown": "龙眠神殿"
    }'::jsonb,
    '{}'::jsonb
);

-- 角色8: 被诅咒的流浪者
INSERT INTO characters (id, name, nickname, age, occupation, height_cm, image_filename, gender, build, race, alignment, status, bloodline, measurements, personality_details, appearance_details, background_details, speech_patterns) VALUES
(
    '12345678-90ab-cdef-1234-567890abcdef',
    '卡西安',
    '影缚者',
    90,
    '流浪者 / 诅咒研究者',
    182,
    'cassian_shadowbound.jpg',
    'MALE',
    'ATHLETIC',
    'HUMAN',
    'CHAOTIC_NEUTRAL',
    'ALIVE',
    'CURSED',
    '{}'::jsonb,
    '{
        "core_traits": ["愤世嫉俗", "坚忍", "敏锐", "有强烈的求生欲", "渴望救赎"],
        "mbti": "INTJ"
    }'::jsonb,
    '{
        "hair": "乌鸦般的黑色乱发，其中夹杂着几缕因诅咒而生的银丝",
        "eyes": "深灰色的眼眸，仿佛藏着无尽的疲惫与秘密",
        "clothing_style": "实用的深色旅行装，一件磨损的皮质风衣从不离身"
    }'::jsonb,
    '{
        "hometown": "已成废墟的“灰烬村”"
    }'::jsonb,
    '{}'::jsonb
);

-- 角色9: 虔诚的月神祭司
INSERT INTO characters (id, name, nickname, age, occupation, height_cm, image_filename, gender, build, race, alignment, status, bloodline, measurements, personality_details, appearance_details, background_details, speech_patterns) VALUES
(
    '23456789-0abc-def1-2345-67890abcdef1',
    '塞拉菲娜',
    '月光咏者',
    350,
    '月神殿的大祭司 / 治愈者',
    170,
    'seraphina_moonsinger.jpg',
    'FEMALE',
    'SLIM',
    'ELF',
    'NEUTRAL_GOOD',
    'ALIVE',
    'DIVINE',
    '{
        "bust_cm": 88,
        "waist_cm": 62,
        "hip_cm": 90
    }'::jsonb,
    '{
        "core_traits": ["温和", "富有同情心", "坚定", "无私", "信仰虔诚"],
        "mbti": "ISFJ"
    }'::jsonb,
    '{
        "hair": "银色的长发，如同流动的月光，常常用花朵和藤蔓装饰",
        "eyes": "湖水般清澈的蓝色眼眸，充满了善意",
        "clothing_style": "飘逸的白色祭司袍，上面用银线绣着月亮的循环图案"
    }'::jsonb,
    '{
        "hometown": "月光林地"
    }'::jsonb,
    '{
        "tone": "声音轻柔但充满力量，总是能安抚人心"
    }'::jsonb
);

-- 角色10: 油滑的港口走私贩
INSERT INTO characters (id, name, nickname, age, occupation, height_cm, image_filename, gender, build, race, alignment, status, bloodline, measurements, personality_details, appearance_details, background_details, speech_patterns) VALUES
(
    '34567890-abcd-ef12-3456-7890abcdef12',
    '芬恩',
    '快手',
    28,
    '走私贩 / 自由商人 / “消息通”',
    179,
    'finn_quickhand.jpg',
    'MALE',
    'AVERAGE',
    'HUMAN',
    'CHAOTIC_NEUTRAL',
    'ALIVE',
    'COMMON',
    '{}'::jsonb,
    '{
        "core_traits": ["机智", "幽默", "善于交际", "极其务实", "对权威不屑一顾"],
        "mbti": "ESTP"
    }'::jsonb,
    '{
        "hair": "棕色的短发，总是有些凌乱",
        "eyes": "灵动的绿色眼睛，透露出狡黠的光芒",
        "clothing_style": "舒适耐磨的皮夹克和裤子，有许多隐藏的口袋"
    }'::jsonb,
    '{
        "hometown": "港口城市“自由港”"
    }'::jsonb,
    '{
        "habits": "喜欢使用俚语和双关语，说话语速快"
    }'::jsonb
);

-- 角色11: 被废黜的贵族
INSERT INTO characters (id, name, nickname, age, occupation, height_cm, image_filename, gender, build, race, alignment, status, bloodline, measurements, personality_details, appearance_details, background_details, speech_patterns) VALUES
(
    '4567890a-bcde-f123-4567-890abcdef123',
    '伊莎贝拉·冯·克洛斯',
    '冬日玫瑰',
    26,
    '没落贵族 / 阴谋家',
    168,
    'isabella_von_kloss.jpg',
    'FEMALE',
    'SLIM',
    'HUMAN',
    'LAWFUL_EVIL',
    'ALIVE',
    'NOBLE',
    '{
        "bust_cm": 85,
        "waist_cm": 59,
        "hip_cm": 88
    }'::jsonb,
    '{
        "core_traits": ["野心勃勃", "精于算计", "高傲", "有魅力", "为达目的不择手段"],
        "mbti": "ENTJ"
    }'::jsonb,
    '{
        "hair": "铂金色的长发，总是梳理得一丝不苟，盘成复杂的发髻",
        "eyes": "冰蓝色的眼眸，锐利而冷漠",
        "clothing_style": "即使处境艰难，也坚持穿着剪裁合体的深色系贵族服饰，保持着最后的体面"
    }'::jsonb,
    '{
        "hometown": "已被篡夺的“鹰巢城”"
    }'::jsonb,
    '{}'::jsonb
);