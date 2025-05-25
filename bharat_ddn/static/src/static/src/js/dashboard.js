
import { registry } from "@web/core/registry";
import { Component } from  "@odoo/owl";
const actionRegistry = registry.category("actions");
class CrmDashboard extends Component {}
CrmDashboard.template = "my_module.CrmDashboard";
actionRegistry.add("my_dashboard_tag", CrmDashboard);



odoo.define('your_module_name.call_python_function', function (require) {
    "use strict";

    var rpc = require('web.rpc');

    // Function to call the Python method and get XML data
    function fetchXMLData() {
        rpc.query({
            route: '/my_custom_route',
            params: {}
        }).then(function (result) {
            // Once the result is fetched, process the XML data
            var xmlData = result.xml_data;
            console.log('XML Data:', xmlData);
            
            // If you need to process the XML, you can use the DOMParser or a library
            var parser = new DOMParser();
            var xmlDoc = parser.parseFromString(xmlData, "application/xml");
            console.log(xmlDoc);
        }).catch(function (error) {
            console.error('Error:', error);
        });
    }

    // Call the function
    fetchXMLData();
});


