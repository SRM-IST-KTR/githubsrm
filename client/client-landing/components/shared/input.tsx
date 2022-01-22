import { Field } from "formik";

import { InputProps } from "../../utils/interfaces";

const Input = (props: InputProps) => {
  switch (props.type) {
    case "text":
    case "email":
    case "password":
    case "textarea": {
      return (
        <div
          className={`${props.onError ? props.wrapperClassName?.onError : ""} ${
            props.wrapperClassName?.default
          }`}
        >
          {props.label && (
            <label
              htmlFor={props.id}
              className={`${
                props.onError ? props.labelClassName?.onError : ""
              } ${props.labelClassName?.default}`}
            >
              {props.label}{" "}
              {props.required && (
                <span className="text-red-500 font-bold">*</span>
              )}
            </label>
          )}
          {props.type === "textarea" ? (
            <Field
              component="textarea"
              name={props.id}
              placeholder={props.placeholder || ""}
              rows={props.textareaOptions?.rows}
              cols={props.textareaOptions?.cols}
              className={`${
                props.onError ? props.inputClassName?.onError : ""
              } ${props.inputClassName?.default}`}
            />
          ) : (
            <Field
              type={props.type}
              name={props.id}
              placeholder={props.placeholder || ""}
              className={`${
                props.onError ? props.inputClassName?.onError : ""
              } ${props.inputClassName?.default}`}
            />
          )}

          {props.description && (
            <p
              className={`${
                props.onError ? props.descriptionClassName?.onError : ""
              } ${props.descriptionClassName?.default}`}
            >
              {props.description}
            </p>
          )}
        </div>
      );
    }
    case "select": {
      return (
        <div
          className={`${props.onError ? props.wrapperClassName?.onError : ""} ${
            props.wrapperClassName?.default
          }`}
        >
          {props.label && (
            <label
              htmlFor={props.id}
              className={`${
                props.onError ? props.labelClassName?.onError : ""
              } ${props.labelClassName?.default}`}
            >
              {props.label}{" "}
              {props.required && (
                <span className="text-red-500 font-bold">*</span>
              )}
            </label>
          )}
          <Field
            as="select"
            name={props.id}
            className={`${props.onError ? props.inputClassName?.onError : ""} ${
              props.inputClassName?.default
            }`}
          >
            <option
              className={props.selectOptions?.optionClassName}
              value="placeholder"
            >
              {props.placeholder}
            </option>
            {props.selectOptions?.options.map((option) => (
              <option
                key={option.value.trim()}
                className={props.selectOptions?.optionClassName}
                value={option.value}
              >
                {option.name}
              </option>
            ))}
          </Field>
        </div>
      );
    }

    case "radio":
    case "checkbox": {
      return (
        <div
          className={`${props.onError ? props.wrapperClassName?.onError : ""} ${
            props.wrapperClassName?.default
          }`}
          role="group"
        >
          {props.label && (
            <label
              className={`${
                props.onError ? props.labelClassName?.onError : ""
              } ${props.labelClassName?.default}`}
            >
              {props.label}
              {props.required && (
                <span className="text-red-500 font-bold"> *</span>
              )}
            </label>
          )}
          {props.selectOptions?.options.map((option) => (
            <label
              key={option.value}
              htmlFor={option.name}
              className={`${
                props.onError ? props.optionClassName?.label?.onError : ""
              } ${props.optionClassName?.label?.default}`}
            >
              <Field
                type={props.type}
                name={props.id}
                placeholder={props.placeholder || ""}
                id={option.value}
                value={option.value}
                className={`${
                  props.onError ? props.optionClassName?.option?.onError : ""
                } ${props.optionClassName?.option?.default}`}
              />
              <div>{option.name} </div>
            </label>
          ))}
        </div>
      );
    }

    default: {
      return <></>;
    }
  }
};

export default Input;
