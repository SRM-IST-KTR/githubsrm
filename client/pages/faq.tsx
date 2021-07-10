import React, { useState } from 'react';
import Head from 'next/head';

import Plus from '../utils/FAQ data/plus';
import Minus from '../utils/FAQ data/minus';

import { Layout } from '../components/shared/index';

import { faqData } from '../utils/FAQ data/faqdata';

const Faq = () => {
  const [question, setquestion] = useState(0);
  return (
    <>
      <Head>
        <title>FAQ</title>
        <meta
          name='description'
          content='A team of 11 students of SRMIST trying to spearhead open-source revolution in SRMIST through the GitHub Community SRM'
        />
      </Head>
      <Layout>
        <div className=''>
          <div className='container mx-auto pt-16 '>
            <div className='text-center  md:pb-10 xl:pb-20'>
              <h1 className='px-2 xl:px-0 xl:text-5xl md:text-3xl text-2xl font-extrabold text-base-blue'>
                Frequently Asked Questions
              </h1>
            </div>
            <div className='w-10/12 mx-auto'>
              <ul>
                {faqData.map((data) => (
                  <li
                    key={data.id}
                    className='py-6 border-base-green border-solid border-b'>
                    <div className='flex justify-between items-center'>
                      <h3 className='text-base-black text-base  md:text-xl font-bold xl:text-2xl w-10/12'>
                        {data.question}
                      </h3>
                      <div
                        className='cursor-pointer'
                        onClick={() =>
                          question === data.id
                            ? setquestion(null)
                            : setquestion(data.id)
                        }>
                        {question === data.id ? <Plus /> : <Minus />}
                      </div>
                    </div>
                    {question === data.id && (
                      <p className='pt-2 md:pt-3  lg:pt-5 text-gray-800 bg-base-smoke p-2 rounded-lg text-sm md:text-base  xl:text-lg '>
                        {data.answer}
                      </p>
                    )}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      </Layout>
    </>
  );
};

export default Faq;
