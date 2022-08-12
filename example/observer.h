/*
 * Observer.h
 *
 *  Created on: 2013-9-3
 *      Author: walter_fan
 */

#ifndef OBSERVER_H_
#define OBSERVER_H_

#include <vector>
#include <mutex>

namespace wfan {

class ISubject;
typedef std::shared_ptr<ISubject> SharedSubjectPtr;

class IObserver: public std::enable_shared_from_this<IObserver> {
public:
    virtual ~IObserver() {};
    virtual void Update(SharedSubjectPtr updatedSubject) = 0;
protected:
    IObserver();
};

typedef std::shared_ptr<IObserver> SharedObserverPtr;
typedef std::weak_ptr<IObserver> WeakObserverPtr;
typedef std::vector<WeakObserverPtr> WeakObserverVector;
typedef std::vector<WeakObserverPtr>::iterator WeakObserverIterator;

class ISubject: public std::enable_shared_from_this<ISubject> {
public:
    virtual ~ISubject() {};
    /**
     * @brief attach observer
     * 
     * @param observer observer to be attached
     */
    virtual void Attach(WeakObserverPtr observer) = 0;
    /**
     * @brief detach observer
     * 
     * @param observer to be detached
     */
    virtual void Detach(WeakObserverPtr observer) = 0;
    /**
     * @brief notify observers
     * 
     */
    virtual void Notify() = 0;
protected:
    ISubject();

};

class CSubject: public ISubject
{
public:
    virtual void Attach(WeakObserverPtr observer);
    virtual void Detach(WeakObserverPtr observer) ;
    virtual void Notify();
private:
    mutable std::mutex m_mutex;
    WeakObserverVector m_observers;
};

} /* namespace wfan */
#endif /* OBSERVER_H_ */