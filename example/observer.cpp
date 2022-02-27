/*
 * Observer.cpp
 *
 *  Created on: 2013-9-3
 *      Author: walter_fan
 */

#include "observer.h"
using namespace std;

namespace wfan {

void CSubject::Attach(WeakObserverPtr pObserver)
{
    std::lock_guard<std::mutex>guard(m_mutex);
	m_observers.push_back(pObserver);
}

void CSubject::Detach(WeakObserverPtr pObserver)
{
    std::lock_guard<std::mutex>guard(m_mutex);
	auto it = m_observers.begin( );
	for (; it != m_observers.end() ; it++ ) {
		m_observers.erase(it);
		break;
	}
}

void CSubject::Notify()
{
    std::lock_guard<std::mutex>guard(m_mutex);

    auto it = m_observers.begin( );
	while (it != m_observers.end()) {
        auto obj(it->lock());
        if (obj) {
            //SharedSubjectPtr sub = make_shared<ISubject>(this);
            obj->Update(shared_from_this());
            ++it;
        } else {
            it = m_observers.erase(it);
        }

	}
}

} /* namespace wfan */
