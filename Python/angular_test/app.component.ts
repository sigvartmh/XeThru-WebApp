import {Component} from 'angular2/core';

interface Wlan {
  ssid: string;
  strength: number;
  password: bool;
}

@Component({
	selector: 'wifi-provisioner',
	template: '
	<li>
	<div class="collapsible-header">{{ wlan.ssid }}</div>
      <div class="collapsible-body">
        <div class="row">
          <div class="col s7">
            <span class="details">MAC: {{ wlan.mac }}</span>
              <input type = 'password' placeholder = 'Password' ng-model ="password" ng-keypress = "(($event.keyCode === 13) && (password !== undefined) )? submit_selection(password) : console.log(test)" />
            <a class="waves-effect waves-light btn xethru_btn " ng-click='submit_selection(password)'>Connect</a>
    </li>
	'
})