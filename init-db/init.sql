-- 这个脚本将在数据库首次创建时自动执行
-- 我们首先连接到正确的数据库
-- \c novel_characters_db;

-- 插入角色 1: 赛博朋克侦探
INSERT INTO characters (id, name, nickname, age, occupation, height_cm, image_filename, gender, build, race, alignment, status, bloodline, measurements, personality_details, appearance_details, background_details, speech_patterns) VALUES
(
    'a1b2c3d4-e5f6-7890-1234-567890abcdef', -- 使用一个固定的 UUID 以便测试
    'Kaelen ''Kae'' Vance', -- 注意：SQL 中单引号需要转义，写成两个单引号 ''
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
    'Lyra Silvanus',
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
    'Grommash Bloodfang',
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