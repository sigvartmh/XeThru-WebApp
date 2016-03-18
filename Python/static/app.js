"use strict";

/***
 *  Define the app and inject any modules we wish to
 *  refer to.
***/
var app = angular.module("XeThru-Wifi", []);

/******************************************************************************\
Function:
    XTController

Dependencies:
    ...

Description:
    Main application controller
\******************************************************************************/
app.controller("XTController", ["XTWlanManager", "$scope", "$location", "$timeout",

    function(XTWlanManager, $scope, $location, $timeout) {
        // Scope variable declaration
        $scope.scan_results              = [];
        $scope.selected_cell             = null;
        $scope.scan_running              = false;
        $scope.network_passcode          = "";
        $scope.show_passcode_entry_field = false;

        // Scope filter definitions
        $scope.orderScanResults = function(cell) {
            console.log("Ordering")
            console.log(cell);
            return parseInt(cell.signal);
        }

        $scope.foo = function() { console.log("foo"); }
        $scope.bar = function() { console.log("bar"); }

        // Scope function definitions
        $scope.rescan = function() {
            console.log("Starting scan");
            $scope.scan_results = [];
            $scope.selected_cell = null;
            $scope.scan_running = true;
            XTWlanManager.rescan_wifi().then(function(response) {
                console.log(response.data);
                if (response.data.status == "SUCCESS") {
                    $scope.scan_results = response.data.scan;
                }
                $scope.scan_results = response.data.scan;
                $scope.scan_running = false;
            });
        }

        $scope.change_selection = function(wlan) {
            $scope.network_passcode = "";
            $scope.selected_cell = wlan;
            $scope.show_passcode_entry_field = (wlan != null) ? true : false;
        }

        $scope.submit_selection = function(password) {
            if (!$scope.selected_cell) return;

            var wifi_info = {
                ssid:      $scope.selected_cell["ssid"],
                password:  password,
            };

            console.log(wifi_info)

            XTWlanManager.enable_wifi(wifi_info).then(function(response) {
                console.log(response.data);
                if (response.data.status == "SUCCESS") {
                    console.log("AP Enabled - nothing left to do...");
                }
            });
        }

        // Defer load the scanned results from the rpi
        $scope.rescan();
    }]
);

/*****************************************************************************\
    Service to hit the rpi wifi config server
\*****************************************************************************/
app.service("XTWlanManager", ["$http",

    function($http) {
        return {
            rescan_wifi: function() {
                console.log("Rescanning");
                var t = $http.get("wlan/api/scan");
                console.log(t)
                return t;
            },
            enable_wifi: function(wifi_info) {
                return $http.post("/wlan/api/connect", wifi_info);
            }
        };
    }]

);
