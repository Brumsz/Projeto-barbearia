from dataclasses import dataclass

@dataclass
class Cliente:
    id:str
    nome:str

    def __post_init__(self):
        if not self.nome:
            raise ValueError('Preencha o campo nome!')


    
