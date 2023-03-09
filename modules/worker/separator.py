# -*- coding: utf-8 -*-

from modules import Base
from modules.file.serifu import Serifu
from modules.file.sep_serifu import SepSerifu
from modules.file.jimaku import Jimaku
from modules.file.raw_jimaku import RawJimaku

class Separator(Base):
    def __init__(self, project):
        super().__init__(project)
        self.actor = self.project.actor
        self.engine = self.project.engine
        self.serifu = Serifu(self.project)
        self.p_serifu = {}
        self.jimaku = Jimaku(self.project)
        self.raw_jimaku = RawJimaku(self.project)

    def _create_p_serifu(self, key: str, engine: str, actor: str) -> SepSerifu:
        self.p_serifu[key]: SepSerifu = SepSerifu(self.project, key, engine, actor)
        self.p_serifu[key].open_write()

        return self.p_serifu[key]

    def _get_p_serifu(self, engine: str, actor: str) -> SepSerifu:
        key: str = f'{engine}_{actor}' if self.engine.is_sep(engine) else engine

        if key in self.p_serifu:
            return self.p_serifu[key]

        return self._create_p_serifu(key, engine, actor)

    def separate(self):
        self.serifu.load()

        actor = self.actor.first_name()
        serifu = ''

        self.jimaku.open_write()
        self.raw_jimaku.open_write()

        for serifu_line in self.serifu.lines:
            actor, serifu = self.serifu.pair(serifu_line, actor)
            real_actor = self.actor.real_name(actor)
            engine = self.actor.engine(actor)
            jimaku = self.serifu.sanitize(serifu, engine)

            # voice_engineが"VP(VOICEPEAK)"の場合は、声優名も追加し、セリフファイルから声優名を削除
            # (VOICEPEAKの場合は1声優のみのため)
            p_serifu: SepSerifu = self._get_p_serifu(engine, real_actor)
            p_serifu.write(serifu)

            self.jimaku.write(real_actor, jimaku, engine)
            self.raw_jimaku.write(actor, jimaku)

        self.jimaku.close()
        self.raw_jimaku.close()

        for name in self.p_serifu.keys():
            self.p_serifu[name].close()

        self.p_serifu = {}

        return True
