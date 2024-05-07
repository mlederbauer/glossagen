"""Example module to get you started."""


def hello_smiles(smiles: str) -> str:
    """
    Return a greeting string that incorporates the given smiles.

    Parameters
    ----------
    smiles : str
        A text string representing a SMILES (Simplified
        Molecular Input Line Entry System) notation or any string.

    Returns
    -------
    str
        A greeting message incorporating the input smiles.

    Examples
    --------
    >>> hello_smiles("C(=O)O")
    'Hello, C(=O)O!'
    """
    return f"Hello, {smiles}!"


if __name__ == "__main__":
    print(hello_smiles("C(=O)O"))
