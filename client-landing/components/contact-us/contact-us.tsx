import { useState } from "react";
import { Formik, Form, FormikState } from "formik";
import Markdown from "react-markdown";

import { Input } from "../shared";
import { ContactUsFormData } from "../../utils/interfaces";
import {
  contactUsInputs,
  contactUsValidation,
  customInputClasses,
} from "../../utils/constants";
import { LoadingIcon } from "../../utils/icons";
import { postContactUs } from "../../services/api";
import { successToast } from "../../utils/functions/toast";

const ContactUs = () => {
  let [loading, setLoading] = useState<boolean>(false);

  //@ts-ignore
  const initialValues: ContactUsFormData = {
    name: "",
    email: "",
    phone_number: "",
    message: "",
  };

  const submitValues = async (
    values: ContactUsFormData,
    resetForm: (nextState?: Partial<FormikState<ContactUsFormData>>) => void
  ) => {
    setLoading(true);
    const res = await postContactUs(values);
    if (res) {
      successToast("Query has been Submitted!");
      resetForm({ values: { ...initialValues } });
      setLoading(false);
      return;
    }
    setLoading(false);
  };

  return (
    <div>
      <div className="font-medium">
        <h1 className="text-2xl lg:text-4xl font-extrabold text-base-blue">
          Contact Us
        </h1>
        <h2 className="text-base lg:text-xl mt-2 text-gray-800">
          Have Doubts? Reach out to us.
        </h2>
      </div>

      <Formik
        initialValues={initialValues}
        onSubmit={(values, { resetForm }) => submitValues(values, resetForm)}
        validationSchema={contactUsValidation}
      >
        {({ errors, touched }) => (
          <Form className="w-full max-w-6xl mt-6 mx-auto">
            <div>
              {contactUsInputs.map((section) => (
                <div
                  key={section.length}
                  className="flex w-full flex-col lg:flex-row"
                >
                  {section.map((field) => (
                    <Input
                      key={field.id}
                      {...field}
                      onError={Object.keys(errors)
                        .filter((i) => touched[i])
                        .includes(field.id)}
                      {...customInputClasses}
                    />
                  ))}
                </div>
              ))}

              {Object.keys(errors).map((error) => {
                if (touched[error]) {
                  return (
                    <Markdown
                      key={error.trim()}
                      className="text-red-500 my-2 lg:my-1"
                    >
                      {errors[error] as string}
                    </Markdown>
                  );
                }
              })}

              <div className="flex mt-4 justify-center lg:justify-end">
                <button
                  disabled={Object.keys(errors).length > 0 || loading}
                  type="submit"
                  className={`${
                    Object.keys(errors).length > 0 || loading
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

export default ContactUs;
