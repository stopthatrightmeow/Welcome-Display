function updateClock ()
{
  var currentTime = new Date ( );

  var currentHours = currentTime.getHours ( );
  var currentMinutes = currentTime.getMinutes ( );

  // Pad the minutes and seconds with leading zeros, if required
  currentMinutes = ( currentMinutes < 10 ? "0" : "" ) + currentMinutes;

  // Compose the string for display
  var currentTimeString = currentHours + ":" + currentMinutes;

  // Update the time display
  document.getElementById("clock").firstChild.nodeValue = currentTimeString;
}