function getElementsByIds(ids) {
  var result = [];
  ids.forEach(function(id) {
    result.push(document.getElementById(id));
  });
  return result;
}

function testSelectorIdsMatch(selector, ids, testName) {
  test(function(){
    var elements = document.querySelectorAll(selector);
    //assert_unreached('one: ' + JSON.stringify([...elements], null, 2) + '\n\ntwo: ' + JSON.stringify(getElementsByIds(ids), null, 2));
    const one = [...elements];
    const two = getElementsByIds(ids);
    console.log('one:');
    for (let i = 0; i < one.length; i++) {
      console.log('[' + i + '] ' + one[i]);
    }
    console.log('two:');
    for (let i = 0; i < two.length; i++) {
      console.log('[' + i + '] ' + two[i]);
    }
    assert_array_equals([...elements], getElementsByIds(ids));
  }, testName);
}

function testSelectorElementsMatch(selector, elements, testName) {
  test(function(){
    assert_array_equals([...document.querySelectorAll(selector)], elements);
  }, testName);
}
