import React, { useState } from 'react';
import Plus from '../../utils/FAQ data/plus';
import Minus from '../../utils/FAQ data/minus';

import { faqData } from '../../utils/FAQ data/faqdata';

const FaqComponent = () => {
  const [question, setQuestion] = useState(0);
  return (
    <div>
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
                  <h3 className='text-base-black text-base md:text-xl font-bold xl:text-2xl w-10/12'>
                    {data.question}
                  </h3>
                  <div
                    className='cursor-pointer'
                    onClick={() =>
                      question === data.id
                        ? setQuestion(null)
                        : setQuestion(data.id)
                    }>
                    {question === data.id ? <Plus /> : <Minus />}
                  </div>
                </div>
                {question === data.id && (
                  <p className='pt-2 md:pt-3 lg:pt-2 text-gray-800 bg-base-smoke p-2 rounded-lg text-sm md:text-base  xl:text-lg mt-2'>
                    {data.answer}
                  </p>
                )}
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
};

export default FaqComponent;
