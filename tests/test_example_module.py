from glossagen.cli import hello_world


# Test the function
def test_hello_smiles():
    assert hello_world("C(=O)O") == "Hello C(=O)O", "Test failed: SMILES input"
