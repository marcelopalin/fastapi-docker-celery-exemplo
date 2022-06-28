"""
    Description:

    Comandos de Diretório em Geral

    Author:           @Palin
    Created:          2021-11-08
    Copyright:        (c) Ampere Consultoria Ltda
"""

try:
    import shutil
    from pathlib import Path
    from shutil import which
    from typing import Union
except ImportError as error:
    print(error)
    print(f"error.name: {error.name}")
    print(f"error.path: {error.path}")


def is_installed(path_to_exe: str):
    """Verifica se o executável `path_to_exe` foi encontrado."""
    return which(path_to_exe) is not None


def inicializa_diretorio(str_pathdir: str, reset_dir: bool = False) -> Union[bool, str]:
    """Verifica se o diretório existe caso contrário cria ele
    e caso a opção reset esteja ativada o diretório é removido
    e criado novamente.

    Args:
        str_pathdir (str): string com o caminho do diretório Ex: Saida/downloads.
        O caminho é relativo ao diretório base do projeto.
        reset (bool): caso deseja deletá-lo e criá-lo novamente marque como True.

    Returns:
        bool: True para sucesso e False caso de Erro
        str: mensagem de Sucesso ou Erro
    """
    PATH_DIR = Path(str_pathdir)
    if reset_dir:
        try:
            if PATH_DIR.is_dir():
                shutil.rmtree(PATH_DIR)
        except OSError as e:
            msg = f"Erro: não pode deletar o diretório {str_pathdir}"
            return False, msg
    # Cria o diretório caso não existe.
    Path(PATH_DIR).mkdir(exist_ok=True, parents=True)
