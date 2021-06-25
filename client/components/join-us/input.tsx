import { Field } from "formik";

import { InputProps } from "../../utils/interfaces";

const Input = (props: InputProps) => {
  switch (props.type) {
    case "text":
    case "email":
    case "textarea": {
      return (
        <div
          className={
            props.onError
              ? props.wrapperClassName?.onError
              : props.wrapperClassName?.default
          }
        >
          {props.label && (
            <label
              htmlFor={props.id}
              className={
                props.onError
                  ? props.labelClassName?.onError
                  : props.labelClassName?.default
              }
            >
              {props.label}
            </label>
          )}
          {props.type === "textarea" ? (
            <Field
              component="textarea"
              name={props.id}
              placeholder={props.placeholder || ""}
              rows={props.textareaOptions?.rows}
              cols={props.textareaOptions?.cols}
              className={
                props.onError
                  ? props.inputClassName?.onError
                  : props.inputClassName?.default
              }
            />
          ) : (
            <Field
              type={props.type}
              name={props.id}
              placeholder={props.placeholder || ""}
              className={
                props.onError
                  ? props.inputClassName?.onError
                  : props.inputClassName?.default
              }
            />
          )}
        </div>
      );
    }
    case "select": {
      return (
        <div
          className={
            props.onError
              ? props.wrapperClassName?.onError
              : props.wrapperClassName?.default
          }
        >
          {props.label && (
            <label
              htmlFor={props.id}
              className={
                props.onError
                  ? props.labelClassName?.onError
                  : props.labelClassName?.default
              }
            >
              {props.label}
            </label>
          )}
          <select
            name={props.id}
            id={props.id}
            className={
              props.onError
                ? props.labelClassName?.onError
                : props.labelClassName?.default
            }
          >
            {props.selectOptions?.options.map((option) => (
              <option
                key={option.value.trim()}
                className={props.selectOptions?.optionClassName}
              >
                {option.name}
              </option>
            ))}
          </select>
        </div>
      );
    }
    default: {
      return <></>;
    }
  }
};

export default Input;
