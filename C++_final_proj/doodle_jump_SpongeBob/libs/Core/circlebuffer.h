#ifndef CIRCLEBUFFER_H
#define CIRCLEBUFFER_H

#include <QDebug>
#include "core_global.h"


template<class T>
class CORE_EXPORT CircleBuffer{
public:
    CircleBuffer(int size=6*100000) : capacity(size) , m_data(size) {}
    bool push(const T& a);
    T pop(bool *ok = nullptr);
    bool isEmpty() const;
    int get_capacity();
    int get_write_pos();
    int get_read_pos();
    T peek();
    void ClearToSaveZone();
    const double upper_bound=0.8;
    const double lower_bound=0.7;
private:
    std::vector<T> m_data;
    int write_pos = 0;
    int capacity;
    int read_pos = 0;
    bool m_isEmpty = true;
    int now_in_buffer = 0;
};

template<class T>
T CircleBuffer<T>::peek()
{
   if (m_isEmpty)
   {
       return T();
   }
   if (write_pos==0)
   {
       return m_data[capacity-1];
   }
   else
   {
       return m_data[write_pos-1];
   }
}

template<class T>
int CircleBuffer<T>::get_capacity()
{
    return capacity;
}

template<class T>
int CircleBuffer<T>::get_read_pos()
{
    return capacity;
}

template<class T>
int CircleBuffer<T>::get_write_pos()
{
    return write_pos;
}

template<class T>
void CircleBuffer<T>::ClearToSaveZone()
{
    if((double(now_in_buffer)/double(capacity))>=upper_bound)
    {
        read_pos =(read_pos+capacity/10)%capacity;
    }
    return;
}

template<class T>
bool CircleBuffer<T>::push(const T &a) {
    now_in_buffer++;
    m_data[write_pos] = a;
    write_pos = (write_pos+1) % capacity;
    m_isEmpty = false;
    return true;
}

template<class T>
T CircleBuffer<T>::pop(bool *ok) {
    if (m_isEmpty){
        if (ok!=nullptr) *ok = false;
        return T();
    }
    now_in_buffer--;
    int rpos = read_pos;
    read_pos =  (read_pos+1) % capacity;
    if (read_pos == write_pos) m_isEmpty = true;
    if (ok!=nullptr) *ok = true;
    return m_data[rpos];
}

template<class T>
bool CircleBuffer<T>::isEmpty() const {
    return m_isEmpty;
}

#endif // CIRCLEBUFFER_H
