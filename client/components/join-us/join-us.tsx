import React, { useState } from "react";
import { Formik, Form } from "formik";
import * as Yup from "yup";
import Markdown from "react-markdown";

import { Section, Input } from "./";
import {
  maintainerInputs,
  inputClassName,
  inputClassNameError,
  labelClassName,
  wrapperClassName,
} from "../../utils/constants";

const Register = () => {
  let [stage, setStage] = useState<number>(0);

  const validationSchema = Yup.object().shape({
    name: Yup.string().trim().required("**Name**: Missing"),
    email: Yup.string()
      .trim()
      .required("**Email**: Missing")
      .email("Should be a valid email."),
    srm_email: Yup.string().trim().required("**SRM Email ID**: Missing"),
    github_id: Yup.string().trim().required("**GitHub ID**: Missing"),
    reg_number: Yup.string()
      .trim()
      .required("**Registration Number**: Missing"),
    branch: Yup.string().trim().required("**Branch**: Missing"),
    project_url: Yup.string().trim().required("**Project**: Missing"),
    poa: Yup.string().trim().required("**Feature or Bugfix:** Missing"),
  });

  type FormData = Partial<Yup.InferType<typeof validationSchema>>;

  const initialValues: FormData = {};

  const submitValues = (values: FormData) => {
    //*INFO: api call here
    console.log(values);
  };

  const changePage = (next: boolean) => {
    if (next) {
      if (stage !== maintainerInputs.length - 1) setStage(stage + 1);
    } else {
      if (stage !== 0) setStage(stage - 1);
    }
  };

  const errorInputId = (ids: string[], errors: string[]): boolean =>
    ids.some((id) => errors.includes(id));

  return (
    <div>
      <div className="font-medium">
        <h1 className="text-4xl">Big text here</h1>
        <h2 className="text-xl mt-2">small text here</h2>
      </div>

      <Formik
        initialValues={initialValues}
        onSubmit={submitValues}
        validationSchema={validationSchema}
      >
        {({ errors, touched }) => (
          <Form className="w-11/12 my-8 mx-auto">
            <>
              <div className="flex justify-evenly">
                <div className="w-4/12 flex flex-col items-center justify-between min-h-lg border-r-2">
                  {maintainerInputs.map((item, index) => (
                    <Section
                      key={item.section}
                      name={item.section}
                      description={item.description}
                      icon={item.icon}
                      isActive={stage === index}
                      setActive={() => setStage(index)}
                      onError={errorInputId(
                        item.inputs.map((i) => i.id),
                        Object.keys(errors).filter((i) => touched[i])
                      )}
                    />
                  ))}
                </div>

                <div className="w-full max-w-3xl flex flex-col justify-between">
                  <div>
                    {maintainerInputs.map((section, index) => (
                      <div
                        key={section.inputs[0].id}
                        className={`${
                          stage !== index ? "hidden" : ""
                        } flex w-11/12 mx-auto flex-col`}
                      >
                        {section.inputs.map((field) => (
                          <Input
                            onError={Object.keys(errors)
                              .filter((i) => touched[i])
                              .includes(field.id)}
                            key={field.id}
                            {...field}
                            wrapperClassName={{
                              default: wrapperClassName,
                              onError: wrapperClassName,
                            }}
                            inputClassName={{
                              default: inputClassName,
                              onError: inputClassNameError,
                            }}
                            labelClassName={{ default: labelClassName }}
                          />
                        ))}
                      </div>
                    ))}
                  </div>

                  <div className="w-11/12 mx-auto h-full pb-6 flex flex-col justify-end">
                    {Object.keys(errors).map((error) => {
                      if (touched[error]) {
                        return (
                          <Markdown className="text-red-500 my-1">
                            {errors[error] as string}
                          </Markdown>
                        );
                      }
                    })}
                  </div>

                  <div>
                    <div className="grid grid-cols-3 gap-x-16 items-center justify-center">
                      <div />
                      {stage == 0 && <div />}
                      {stage !== 0 && (
                        <button
                          type="button"
                          onClick={() => changePage(false)}
                          className="bg-base-smoke py-3 rounded-lg"
                        >
                          Back
                        </button>
                      )}

                      {stage !== maintainerInputs.length - 1 ? (
                        <button
                          type="button"
                          onClick={() => changePage(true)}
                          className="text-white bg-base-black py-3 font-semibold rounded-lg"
                        >
                          Next
                        </button>
                      ) : (
                        <button
                          disabled={Object.keys(errors).length > 0}
                          type="submit"
                          className={`${
                            Object.keys(errors).length > 0
                              ? "cursor-not-allowed bg-opacity-70"
                              : "cursor-pointer"
                          } text-white bg-base-green py-3 font-semibold rounded-lg`}
                        >
                          Submit
                        </button>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            </>
          </Form>
        )}
      </Formik>
    </div>
  );
};

export default Register;
