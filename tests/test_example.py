# Make sure test names start with 'test_'
def test_numbers():
  number1 = 4
  number2 = 2 + 2
  # Test with assert
  assert number1 == number2
  
 def test_string():
  sentence = "Hey there"
  # This should fail
  assert sentence == "Hi there"
