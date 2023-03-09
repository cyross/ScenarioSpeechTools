# -*- coding: utf-8 -*-

from modules import Base
from modules.io import *

class Builder(Base):
    def __init__(self, project):
        super().__init__(project)
        self.actor = self.project.actor
        self.engine = self.project.engine

    def _filter_actor(self, actor: str, engine: str) -> bool:
        return self.actor.engine(actor) == engine and actor[0] != "["

    def _generate_separate_by_actors(self, engine: str) -> list[str]:
        return list(filter(lambda actor: self._filter_actor(actor, engine), self.actor.names))

    def _create_out_dirs(self):
        for engine in self.engine.names:
            if self.engine.is_sep(engine):
                actors = self._generate_separate_by_actors(engine)

                for name in actors:
                    make_dir(self.io.join_output_dir(f'{engine}_{self.actor.sanitize(name)}'))
            else:
                make_dir(self.io.join_output_dir(engine))

    def build(self):
        make_dir(self.io.project_dir)
        make_dir(self.io.input_dir)
        make_dir(self.io.output_dir)
        make_dir(self.io.renamed_dir)
        self._create_out_dirs()
        create_file(self.io.base_serifu_filepath)

        return True

