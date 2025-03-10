/////////////////////
// Alarm functions //
/////////////////////

function addDisplayedAlarm(data) {
  const alarmList = document.getElementById("alarm_list");
  const alarmItem = document.createElement("nav");
  alarmItem.classList.add("fieldset", "alarm-item", "wrap");
  alarmItem.innerHTML = `
  <input hidden="" class="alarm-id"/>
  <div class="field border">
    <input class="alarm-date" type="date"/>
  </div>
  <div class="field border">
    <input class="alarm-time" type="time"/>
  </div>
  <div class="field border label">
    <input class="alarm-label"/>
    <label>Label</label>
  </div>
  <nav class="max right-align">
    <label class="switch icon"><input type="checkbox" class="alarm-enabled" onclick="enableAlarm(this)"><span><i>close</i><i>done</i></span></label>
    <button class="border square round" onclick="saveAlarm(this)"><i>save</i></button>
    <button class="border round primary" onclick="removeDisplayedAlarm(this)">Remove</button>
  </nav>
`;
  if (data.id) alarmItem.getElementsByClassName("alarm-id")[0].value = data.id;
  if (data.date) alarmItem.getElementsByClassName("alarm-date")[0].value = data.date;
  if (data.time) alarmItem.getElementsByClassName("alarm-time")[0].value = data.time;
  if (data.label) alarmItem.getElementsByClassName("alarm-label")[0].value = data.label;
  if (data.label) alarmItem.getElementsByClassName("alarm-enabled")[0].checked = data.enabled;
  alarmList.appendChild(alarmItem);
}

function createAlarm(name="Alarm") {
  const now = new Date();
  // Format date as yy-MM-DD
  const formattedDate = now.toISOString().split('T')[0];
  // Format time as HH:MM
  const formattedTime = now.toLocaleTimeString('en-GB', {
    hour: '2-digit',
    minute: '2-digit',
    hour12: false
  });

  const alarm = {
    "date": formattedDate,
    "time": formattedTime,
    "label": name
  }

  fetch('/api/alarms', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify([alarm]),
  })
      .then(response => response.json())
      .then(data => {
        console.log(data);
        removeDisplayedAlarms()
        getAllAlarms()
      })
      .catch(error => {
        console.error('Error:', error)
    });
}

function saveAlarm(button) {
  let alarm_item = getAlarmItem(button);
  const alarm_id = getAlarmId(alarm_item)
  const data = {
    "date": alarm_item.getElementsByClassName("alarm-date")[0].value,
    "time": alarm_item.getElementsByClassName("alarm-time")[0].value,
    "label": alarm_item.getElementsByClassName("alarm-label")[0].value
  }

  fetch('/api/alarms/' + alarm_id, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
  })
      .then(response => response.json())
      .then(data => {
        ui("#alarm-saved")
      })
      .catch(error => console.error('Error:', error));
}

function enableAlarm(checkbox) {
  let alarm_item = getAlarmItem(checkbox);
  const alarm_id = getAlarmId(alarm_item)
  const enabled = checkbox.checked
  fetch('/api/alarms/' + alarm_id + '/enable', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({'enabled': enabled})
  })
      .then(response => response.json())
      .then(data => {
        if (enabled) {
          ui("#alarm-enabled")
        } else {
          ui("#alarm-disabled")
        }
      })
      .catch(error => console.error('Error:', error));
}

function removeDisplayedAlarm(button) {
  let alarm_item = getAlarmItem(button)
  fetch('/api/alarms/' + getAlarmId(alarm_item), {
    method: 'DELETE',
    headers: { 'Content-Type': 'application/json' },
  })
    .then(response => response.json())
    .then(() => {
        getAlarmItem(button).remove();
    })
    .catch(error => console.error('Error:', error));

}

function removeDisplayedAlarms() {
  document.querySelectorAll('.alarm-item').forEach(element => element.remove());
}

function getAllAlarms() {
  fetch('/api/alarms', {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
  })
      .then(response => response.json())
      .then(data => {
        console.log(data);
        for (const alarm of data['alarms']) {
          addDisplayedAlarm(alarm);
        }
      })
      .catch(error => {
        console.error('Error:', error)
      });
}

function getAlarmItem(el) {
  return el.closest('.alarm-item')
}

function getAlarmId(alarm_item) {
  return alarm_item.getElementsByClassName("alarm-id")[0].value
}

////////////////
// Entrypoint //
////////////////

// Add an initial alarm field on page load
getAllAlarms()