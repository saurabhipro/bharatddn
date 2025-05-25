/** @odoo-module **/

import { Component } from "@odoo/owl";

export class KpiCard extends Component {
    static template = "ddn.KpiCardTemplate";
    static props = {
        name: { type: String },
        value: { type: Number },
        bgClass: { type: String, optional: true }
    };
}

// No need to register this as an action since it's a child component
