import { useState } from "react";
import { Formik, Form } from "formik";
import Markdown from "react-markdown";

import { Input } from "../shared";
import { ContactUsFormData } from "../../utils/interfaces";
import * as FormConstants from "../../utils/constants";
import { LoadingIcon } from "../../utils/icons";
import { postContactUs } from "../../services/api";

const Right = () => {
  let [loading, setLoading] = useState<boolean>(false);

  const initialValues: Partial<ContactUsFormData> = {};

  const submitValues = async (values: ContactUsFormData) => {
    setLoading(true);
    try {
      console.log(values);
      const res = await postContactUs(values);
    } catch (error) {}

    setLoading(false);
  };

  return (
    <div>
      <div className="font-medium">
        <h1 className="text-4xl">Contact Us</h1>
        <h2 className="text-xl mt-2">descrip</h2>
      </div>
      <Formik
        initialValues={initialValues}
        onSubmit={submitValues}
        validationSchema={FormConstants.contactUsValidation}
      >
        {({ errors, touched }) => (
          <Form className="w-11/12 max-w-6xl my-8 mx-auto">
            <div>
              {FormConstants.contactUsInputs.map((section) => (
                <div className="my-6 flex w-full">
                  {section.map((field) => (
                    <Input
                      key={field.id}
                      {...field}
                      onError={Object.keys(errors)
                        .filter((i) => touched[i])
                        .includes(field.id)}
                      wrapperClassName={{
                        default: FormConstants.wrapperClassName,
                        onError: FormConstants.wrapperClassName,
                      }}
                      inputClassName={{
                        default: FormConstants.inputClassName,
                        onError: FormConstants.inputClassNameError,
                      }}
                      labelClassName={{
                        default: FormConstants.labelClassName,
                      }}
                    />
                  ))}
                </div>
              ))}

              {Object.keys(errors).map((error) => {
                if (touched[error]) {
                  return (
                    <Markdown key={error.trim()} className="text-red-500 my-1">
                      {errors[error] as string}
                    </Markdown>
                  );
                }
              })}

              <div className="flex justify-end">
                <button
                  disabled={Object.keys(errors).length > 0}
                  type="submit"
                  className={`${
                    Object.keys(errors).length > 0
                      ? "cursor-not-allowed bg-opacity-70"
                      : "cursor-pointer"
                  } text-white bg-base-teal w-32 py-2 font-semibold rounded-lg`}
                >
                  {!loading ? (
                    "Submit"
                  ) : (
                    <span className="flex w-6 mx-auto">
                      <LoadingIcon />
                    </span>
                  )}
                </button>
              </div>
            </div>
          </Form>
        )}
      </Formik>
    </div>
  );
};

export default Right;
