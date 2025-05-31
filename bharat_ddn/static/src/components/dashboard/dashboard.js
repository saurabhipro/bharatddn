/** @odoo-module **/

import { registry } from "@web/core/registry";
import { KpiCard } from "../kpi_card/kpi_card";
import { PropertyMapView } from "../google_map/property_map";
import { Component, onWillStart, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export class OwlCrmDashboard extends Component {
    static components = { KpiCard, PropertyMapView };

    setup() {
        this.orm = useService("orm");
        this.state = useState({
            property_info: {
                ward_data: [], // Initialize ward_data as an empty array
                // ... other property info fields
            },
            error: null,
            isLoading: true
        });

        onWillStart(async () => {
            await this.loadDashboardData();
        });
    }

    async loadDashboardData() {
        try {
            // Property status wise data
            const propertyDetails = await this.orm.call(
                'ddn.property.info',
                'get_dashboard_data',
                [],
                {}
            );
            
            console.log("propertyDetails - ", propertyDetails);
            
            if (propertyDetails && propertyDetails.length > 0) {
                const data = propertyDetails[0];
                
                // Ensure ward_data is always an array
                this.state.property_info = {
                    ...data,
                    ward_data: Array.isArray(data.ward_data) ? data.ward_data : []
                };
                
                console.log("Processed ward data:", this.state.property_info.ward_data);
            } else {
                console.warn("No property details found.");
                this.state.property_info.ward_data = [];
            }
        } catch (error) {
            console.error("Error loading dashboard data:", error);
            this.state.error = error.message || "Failed to load dashboard data";
        } finally {
            this.state.isLoading = false;
        }
    }

    /**
     * Helper method to safely get ward data
     * @returns {Array} ward data array or empty array if not available
     */
    getWardData() {
        return this.state.property_info?.ward_data || [];
    }
}

// Define the template for the component
OwlCrmDashboard.template = 'smkc.OwlCrmTemplate';

// Register the component
registry.category("actions").add("ddn.crm_dashboard_tag", OwlCrmDashboard);