"""初始化经典方剂数据库"""
import asyncio
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from sqlalchemy.ext.asyncio import AsyncSession
from core.database import engine, Base, AsyncSessionLocal
from api.models.prescription import ClassicFormula, ClassicFormulaHerb
from api.models.patient import Patient
from api.models.visit import Visit

FORMULAS = [
    {
        "name": "桂枝汤", "source": "伤寒论", 
        "syndrome": "太阳中风，发热汗出，恶风，脉浮缓",
        "indication": "解肌祛风，调和营卫",
        "cooking_notes": "水七升，微火煮取三升，温服一升，服已须臾，啜热稀粥一升余",
        "herbs": [
            {"herb_name": "桂枝", "dosage_liang": 3, "dosage_g": 15},
            {"herb_name": "芍药", "dosage_liang": 3, "dosage_g": 15},
            {"herb_name": "甘草", "dosage_liang": 2, "dosage_g": 10, "processing": "炙"},
            {"herb_name": "生姜", "dosage_liang": 3, "dosage_g": 15},
            {"herb_name": "大枣", "dosage_liang": 12, "dosage_g": 12, "notes": "12枚，擘"},
        ]
    },
    {
        "name": "麻黄汤", "source": "伤寒论",
        "syndrome": "太阳伤寒，恶寒发热，头身疼痛，无汗而喘，脉浮紧",
        "indication": "发汗解表，宣肺平喘",
        "cooking_notes": "水九升，先煮麻黄减二升，去上沫，内诸药，煮取二升半，温服八合",
        "herbs": [
            {"herb_name": "麻黄", "dosage_liang": 3, "dosage_g": 15, "processing": "先煎去沫"},
            {"herb_name": "桂枝", "dosage_liang": 2, "dosage_g": 10},
            {"herb_name": "甘草", "dosage_liang": 1, "dosage_g": 5, "processing": "炙"},
            {"herb_name": "杏仁", "dosage_liang": 70, "dosage_g": 14, "notes": "70个，去皮尖"},
        ]
    },
    {
        "name": "小柴胡汤", "source": "伤寒论",
        "syndrome": "少阳证，寒热往来，胸胁苦满，默默不欲饮食，心烦喜呕，口苦，咽干，目眩",
        "indication": "和解少阳",
        "cooking_notes": "水一斗二升，煮取六升，去滓，再煎取三升，温服一升，日三服",
        "herbs": [
            {"herb_name": "柴胡", "dosage_liang": 8, "dosage_g": 24},
            {"herb_name": "黄芩", "dosage_liang": 3, "dosage_g": 9},
            {"herb_name": "人参", "dosage_liang": 3, "dosage_g": 9},
            {"herb_name": "甘草", "dosage_liang": 3, "dosage_g": 9, "processing": "炙"},
            {"herb_name": "半夏", "dosage_liang": 0.5, "dosage_g": 9, "notes": "半升，洗"},
            {"herb_name": "生姜", "dosage_liang": 3, "dosage_g": 9},
            {"herb_name": "大枣", "dosage_liang": 12, "dosage_g": 12, "notes": "12枚，擘"},
        ]
    },
    {
        "name": "四逆汤", "source": "伤寒论",
        "syndrome": "少阴病，四肢厥冷，恶寒蜷卧，下利清谷，脉微细",
        "indication": "回阳救逆",
        "cooking_notes": "水三升，煮取一升二合，去滓，分温再服",
        "herbs": [
            {"herb_name": "附子", "dosage_liang": 1, "dosage_g": 15, "processing": "生用，去皮，破八片"},
            {"herb_name": "干姜", "dosage_liang": 1.5, "dosage_g": 8},
            {"herb_name": "甘草", "dosage_liang": 2, "dosage_g": 10, "processing": "炙"},
        ]
    },
    {
        "name": "酸枣仁汤", "source": "金匮要略",
        "syndrome": "虚劳虚烦不得眠，心悸，头目眩晕，咽干口燥，脉细弦",
        "indication": "养血安神，清热除烦",
        "cooking_notes": "水八升，煮酸枣仁得六升，内诸药，煮取三升，分温三服",
        "herbs": [
            {"herb_name": "酸枣仁", "dosage_liang": 2, "dosage_g": 15, "notes": "炒"},
            {"herb_name": "甘草", "dosage_liang": 1, "dosage_g": 3},
            {"herb_name": "知母", "dosage_liang": 2, "dosage_g": 6},
            {"herb_name": "茯苓", "dosage_liang": 2, "dosage_g": 6},
            {"herb_name": "川芎", "dosage_liang": 2, "dosage_g": 6},
        ]
    },
    {
        "name": "大承气汤", "source": "伤寒论",
        "syndrome": "阳明腑实，痞满燥实坚，大便秘结，潮热谵语，腹胀满拒按，脉沉实",
        "indication": "峻下热结",
        "cooking_notes": "水一斗，先煮枳实、厚朴取五升，去滓，内大黄，更煮取二升，去滓，内芒硝",
        "herbs": [
            {"herb_name": "大黄", "dosage_liang": 4, "dosage_g": 12, "processing": "酒洗"},
            {"herb_name": "厚朴", "dosage_liang": 8, "dosage_g": 24, "processing": "去皮，炙"},
            {"herb_name": "枳实", "dosage_liang": 5, "dosage_g": 12, "notes": "5枚，炙"},
            {"herb_name": "芒硝", "dosage_liang": 3, "dosage_g": 9, "notes": "冲服"},
        ]
    },
    {
        "name": "真武汤", "source": "伤寒论",
        "syndrome": "阳虚水泛，畏寒肢厥，小便不利，心下悸，头目眩晕，或浮肿，脉沉",
        "indication": "温阳利水",
        "cooking_notes": "水八升，煮取三升，去滓，温服七合，日三服",
        "herbs": [
            {"herb_name": "茯苓", "dosage_liang": 3, "dosage_g": 9},
            {"herb_name": "芍药", "dosage_liang": 3, "dosage_g": 9},
            {"herb_name": "生姜", "dosage_liang": 3, "dosage_g": 9},
            {"herb_name": "白术", "dosage_liang": 2, "dosage_g": 6},
            {"herb_name": "附子", "dosage_liang": 1, "dosage_g": 9, "processing": "炮，去皮，破八片"},
        ]
    },
    {
        "name": "炙甘草汤", "source": "伤寒论",
        "syndrome": "心动悸，脉结代，虚羸少气，舌光少苔",
        "indication": "益气滋阴，通阳复脉",
        "cooking_notes": "清酒七升，水八升，先煮八味，取三升，去滓，内胶烊消尽，温服一升，日三服",
        "herbs": [
            {"herb_name": "甘草", "dosage_liang": 4, "dosage_g": 12, "processing": "炙"},
            {"herb_name": "生姜", "dosage_liang": 3, "dosage_g": 9},
            {"herb_name": "人参", "dosage_liang": 2, "dosage_g": 6},
            {"herb_name": "生地黄", "dosage_liang": 16, "dosage_g": 48},
            {"herb_name": "桂枝", "dosage_liang": 3, "dosage_g": 9},
            {"herb_name": "阿胶", "dosage_liang": 2, "dosage_g": 6, "processing": "烊化"},
            {"herb_name": "麦门冬", "dosage_liang": 0.5, "dosage_g": 10, "notes": "半升，去心"},
            {"herb_name": "麻仁", "dosage_liang": 0.5, "dosage_g": 10, "notes": "半升"},
            {"herb_name": "大枣", "dosage_liang": 30, "dosage_g": 30, "notes": "30枚"},
        ]
    },
    {
        "name": "理中丸", "source": "伤寒论",
        "syndrome": "脾胃虚寒，自利不渴，呕吐腹痛，腹满不食，脉沉迟",
        "indication": "温中祛寒，补气健脾",
        "cooking_notes": "蜜丸如鸡子黄大，研碎，温水送服；或作汤剂水煎服",
        "herbs": [
            {"herb_name": "人参", "dosage_liang": 3, "dosage_g": 9},
            {"herb_name": "干姜", "dosage_liang": 3, "dosage_g": 9},
            {"herb_name": "甘草", "dosage_liang": 3, "dosage_g": 9, "processing": "炙"},
            {"herb_name": "白术", "dosage_liang": 3, "dosage_g": 9},
        ]
    },
    {
        "name": "黄连阿胶汤", "source": "伤寒论",
        "syndrome": "少阴病，心中烦，不得卧，阴虚火旺，脉细数",
        "indication": "育阴清热，除烦安神",
        "cooking_notes": "水六升，先煮三物，取二升，去滓，内胶烊尽，小冷，内鸡子黄，搅令相得，温服七合",
        "herbs": [
            {"herb_name": "黄连", "dosage_liang": 4, "dosage_g": 12},
            {"herb_name": "黄芩", "dosage_liang": 2, "dosage_g": 6},
            {"herb_name": "芍药", "dosage_liang": 2, "dosage_g": 6},
            {"herb_name": "鸡子黄", "dosage_liang": 2, "dosage_g": 0, "notes": "2枚，后下"},
            {"herb_name": "阿胶", "dosage_liang": 3, "dosage_g": 9, "processing": "烊化"},
        ]
    },
    {
        "name": "当归四逆汤", "source": "伤寒论",
        "syndrome": "手足厥寒，脉细欲绝，血虚寒凝",
        "indication": "温经散寒，养血通脉",
        "cooking_notes": "水八升，煮取三升，去滓，温服一升，日三服",
        "herbs": [
            {"herb_name": "当归", "dosage_liang": 3, "dosage_g": 9},
            {"herb_name": "桂枝", "dosage_liang": 3, "dosage_g": 9},
            {"herb_name": "芍药", "dosage_liang": 3, "dosage_g": 9},
            {"herb_name": "细辛", "dosage_liang": 3, "dosage_g": 3},
            {"herb_name": "甘草", "dosage_liang": 2, "dosage_g": 6, "processing": "炙"},
            {"herb_name": "通草", "dosage_liang": 2, "dosage_g": 6},
            {"herb_name": "大枣", "dosage_liang": 25, "dosage_g": 25, "notes": "25枚"},
        ]
    },
    {
        "name": "乌梅丸", "source": "伤寒论",
        "syndrome": "厥阴病，消渴，气上撞心，心中疼热，饥而不欲食，食则吐蛔，久利",
        "indication": "温脏安蛔",
        "cooking_notes": "苦酒渍乌梅一宿，去核，蒸之五斗米下，饭熟捣成泥，和药令相得，内臼中，与蜜杵二千下，丸如梧桐子大",
        "herbs": [
            {"herb_name": "乌梅", "dosage_liang": 300, "dosage_g": 30, "notes": "300枚"},
            {"herb_name": "细辛", "dosage_liang": 6, "dosage_g": 6},
            {"herb_name": "干姜", "dosage_liang": 10, "dosage_g": 10},
            {"herb_name": "黄连", "dosage_liang": 16, "dosage_g": 16},
            {"herb_name": "当归", "dosage_liang": 4, "dosage_g": 12},
            {"herb_name": "附子", "dosage_liang": 6, "dosage_g": 15, "processing": "炮，去皮"},
            {"herb_name": "蜀椒", "dosage_liang": 4, "dosage_g": 6, "processing": "炒"},
            {"herb_name": "桂枝", "dosage_liang": 6, "dosage_g": 9},
            {"herb_name": "人参", "dosage_liang": 6, "dosage_g": 9},
            {"herb_name": "黄柏", "dosage_liang": 6, "dosage_g": 6},
        ]
    },
]

async def seed():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        # 检查是否已有数据
        from sqlalchemy import select, func
        cnt = await session.execute(select(func.count()).select_from(ClassicFormula))
        if cnt.scalar() > 0:
            print(f"经典方剂已有数据，跳过初始化")
            return

        for f_data in FORMULAS:
            herbs_data = f_data.pop("herbs")
            formula = ClassicFormula(**f_data)
            session.add(formula)
            await session.flush()
            for h in herbs_data:
                herb = ClassicFormulaHerb(formula_id=formula.id, **h)
                session.add(herb)
        await session.commit()
        print(f"✅ 已初始化 {len(FORMULAS)} 个经典方剂")

if __name__ == "__main__":
    asyncio.run(seed())
