import { FormTextFieldProps } from "../../utils/interfaces";
import { Field } from "formik";

export interface FormTextFieldProps {
  id: string;
  label: string;
  placeholder: string;
}

const FormTextField = ({ vals, touched, errors }) => (
  <>
    <label htmlFor={vals.id}>{vals.label}</label>
    <Field
      type={vals.type}
      name={vals.id}
      placeholder={vals.placeholder}
      className={`
${
  touched[vals.id] && errors[vals.id] ? "border-red-500" : "border-gray-300"
} rounded-lg border-2 focus:border-gray-600 w-full py-2 px-4 bg-white text-gray-700 placeholder-gray-400 shadow-sm`}
    />
  </>
);

export default FormTextField;
