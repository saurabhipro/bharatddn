/** @odoo-module **/

import { registry } from "@web/core/registry";
import { _t } from "@web/core/l10n/translation";
import { standardFieldProps } from "@web/views/fields/standard_field_props";
import { formatChar } from "@web/views/fields/formatters";
import { useDynamicPlaceholder } from "@web/views/fields/dynamic_placeholder_hook";
import { useInputField } from "@web/views/fields/input_field_hook";
import { Component, useExternalListener, useRef, useEffect, useState } from "@odoo/owl";
import { usePopover } from "@web/core/popover/popover_hook";
import { localization } from "@web/core/l10n/localization";

import { IconPickerPopover } from "../icon_picker_popover/icon_picker_popover";

export class IconPickerCharField extends Component {

    static template = "sh_font_awesome_icon_picker_widget.IconPickerCharField";
    static props = {
        ...standardFieldProps,
        hidden: { type: Boolean, optional: true },
        placeholder: { type: String, optional: true },
        dynamicPlaceholder: { type: Boolean, optional: true },
    };

    static defaultProps = { dynamicPlaceholder: false, hidden: true };

    setup() {
        this.input = useRef("input");
        this.state = useState(
            {
                searchTerm: "",
                currentIcon: this.formattedValue
            }
        )
        const position = localization.direction === "rtl" ? "bottom" : "left";
        this.popover = usePopover(IconPickerPopover, { position: position });

        if (this.props.dynamicPlaceholder) {
            const dynamicPlaceholder = useDynamicPlaceholder(this.input);
            useExternalListener(document, "keydown", dynamicPlaceholder.onKeydown);
            useEffect(() =>
                dynamicPlaceholder.updateModel(this.props.dynamicPlaceholderModelReferenceField)
            );
        }

        useInputField({
            getValue: () => this.props.record.data[this.props.name] || "",
            parse: (v) => this.parse(v),
        });
    }

    onClickOpenIconPicker(ev) {
        this.popover.open(ev.target, {
            close: () => this.close(),
            state: this.state,
            onSelect: this.onSelect.bind(this),
        });
    }

    get formattedValue() {
        return formatChar(this.props.record.data[this.props.name]);
    }
    onSelect(value) {
        this.state.currentIcon = formatChar(value);
        this.props.record.update({ [this.props.name]: value });
        this.popover.close()
    }
}

export const iconPickerCharField = {
    component: IconPickerCharField,
    supportedTypes: ["char"],
    displayName: _t("Icon Selection"),
    extractProps: ({ attrs, options }) => ({
        dynamicPlaceholder: options.dynamic_placeholder || false,
        placeholder: attrs.placeholder,
    }),
};

registry.category("fields").add("sh_fa_icon_picker_char", iconPickerCharField);
