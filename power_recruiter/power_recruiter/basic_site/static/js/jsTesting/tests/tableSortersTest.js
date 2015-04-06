QUnit.test( "idSorter test", function( assert ) {
  smallerId = function(){};
  biggerId = function(){};
  smallerId.id = -999;
  biggerId.id = 147;
  assert.ok( idSorter(smallerId, biggerId) == -1, "< test" );
  assert.ok( idSorter(biggerId, smallerId) == 1, "> test" );
  assert.ok( idSorter(biggerId, biggerId) == 0, "= test" );
});

QUnit.test( "nameSorter test", function( assert ) {
  smallerName = function(){};
  biggerName = function(){};
  smallerName.candidate_name = "Jan Kowalski";
  biggerName.candidate_name = "Zofia Zazalska";
  assert.ok( nameSorter(smallerName, biggerName) == -1, "< test" );
  assert.ok( nameSorter(biggerName, smallerName) == 1, "> test" );
  assert.ok( nameSorter(biggerName, biggerName) == 0, "= test" );
});


QUnit.test( "stateSorter test", function( assert ) {
  smallerState = function(){};
  biggerState = function(){};
  smallerState.state_name = "Pierwszy";
  biggerState.state_name = "Trzeci";
  assert.ok( stateSorter(smallerState, biggerState) == -1, "< test" );
  assert.ok( stateSorter(biggerState, smallerState) == 1, "> test" );
  assert.ok( stateSorter(biggerState, biggerState) == 0, "= test" );
});